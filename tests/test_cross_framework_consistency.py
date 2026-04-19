"""Cross-framework field consistency tests.

Verifies that every contrib module exposes the same field names for each mixin,
catching drift where one framework uses a different name than the others.

See: https://github.com/hasansezertasan/opinionated-mixins/issues/32
"""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable
from mongoengine.base.fields import BaseField
from odmantic.field import ODMFieldInfo
from opinionated_mixins.contrib import (
    dataclasses as dc_contrib,
)
from opinionated_mixins.contrib import (
    mongoengine as me_contrib,
)
from opinionated_mixins.contrib import (
    odmantic as od_contrib,
)
from opinionated_mixins.contrib import (
    pydantic as pd_contrib,
)
from opinionated_mixins.contrib import (
    sqlalchemy as sa_contrib,
)
from opinionated_mixins.contrib import (
    sqlmodel as sm_contrib,
)
from opinionated_mixins.contrib import (
    wtforms as wt_contrib,
)
from pydantic.fields import FieldInfo as PydanticFieldInfo
from sqlalchemy import Column
from wtforms.fields.core import UnboundField as WTUnboundField

MIXIN_NAMES = ["Announcement", "Feedback", "Lead", "Person", "Template", "User"]

REFERENCE_FRAMEWORK = "pydantic"

# Fields intentionally excluded from specific frameworks.
# Key: (framework, mixin), Value: set of field names to ignore.
EXPECTED_EXCLUSIONS: dict[tuple[str, str], set[str]] = {
    # WTForms collects raw input; password hashing is app-level concern.
    ("wtforms", "User"): {"hashed_password"},
}


def _isinstance_extractor(field_type: type) -> Callable[[type], set[str]]:
    """Create an extractor that finds fields by isinstance check on __dict__."""

    def extract(mixin_cls: type) -> set[str]:
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, field_type)
        }

    return extract


def _dataclass_extractor(mixin_cls: type) -> set[str]:
    return {f.name for f in dataclasses.fields(mixin_cls)}


FRAMEWORKS: dict[str, tuple[object, Callable[[type], set[str]]]] = {
    "pydantic": (pd_contrib, _isinstance_extractor(PydanticFieldInfo)),
    "sqlalchemy": (sa_contrib, _isinstance_extractor(Column)),
    "sqlmodel": (sm_contrib, _isinstance_extractor(Column)),
    "mongoengine": (me_contrib, _isinstance_extractor(BaseField)),
    "odmantic": (od_contrib, _isinstance_extractor(ODMFieldInfo)),
    "wtforms": (wt_contrib, _isinstance_extractor(WTUnboundField)),
    "dataclasses": (dc_contrib, _dataclass_extractor),
}


@pytest.mark.parametrize("mixin_name", MIXIN_NAMES)
def test_all_frameworks_have_same_fields(mixin_name: str) -> None:
    """Each mixin must expose identical field names across all frameworks."""
    fields_by_framework: dict[str, set[str]] = {}
    for fw_name, (module, extractor) in FRAMEWORKS.items():
        mixin_cls = getattr(module, mixin_name)
        fields_by_framework[fw_name] = extractor(mixin_cls)

    reference_fields = fields_by_framework[REFERENCE_FRAMEWORK]

    for fw_name, fields in fields_by_framework.items():
        if fw_name == REFERENCE_FRAMEWORK:
            continue
        excluded = EXPECTED_EXCLUSIONS.get((fw_name, mixin_name), set())
        missing = reference_fields - fields - excluded
        extra = fields - reference_fields
        assert not missing, (
            f"{mixin_name}: {fw_name} missing vs {REFERENCE_FRAMEWORK}: {missing}"
        )
        assert not extra, (
            f"{mixin_name}: {fw_name} extra vs {REFERENCE_FRAMEWORK}: {extra}"
        )


@pytest.mark.parametrize("mixin_name", MIXIN_NAMES)
def test_all_frameworks_export_mixin(mixin_name: str) -> None:
    """Every framework module must export every mixin."""
    for fw_name, (module, _) in FRAMEWORKS.items():
        assert hasattr(module, mixin_name), f"{fw_name} does not export {mixin_name}"


def test_expected_exclusions_are_valid() -> None:
    """Excluded fields must exist in the reference framework's mixin."""
    ref_module = FRAMEWORKS[REFERENCE_FRAMEWORK][0]
    ref_extractor = FRAMEWORKS[REFERENCE_FRAMEWORK][1]
    for (fw_name, mixin_name), excluded_fields in EXPECTED_EXCLUSIONS.items():
        assert fw_name in FRAMEWORKS, f"Unknown framework in exclusions: {fw_name}"
        assert mixin_name in MIXIN_NAMES, f"Unknown mixin in exclusions: {mixin_name}"
        ref_cls = getattr(ref_module, mixin_name)
        ref_fields = ref_extractor(ref_cls)
        stale = excluded_fields - ref_fields
        assert not stale, (
            f"Stale exclusion: {stale} not in {REFERENCE_FRAMEWORK}.{mixin_name}"
        )
