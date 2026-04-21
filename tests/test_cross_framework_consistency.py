"""Cross-framework field consistency tests.

Verifies that every contrib module exposes the same field names for each mixin,
catching drift where one framework uses a different name than the others.

See: https://github.com/hasansezertasan/opinionated-mixins/issues/32
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable
from mongoengine.base.fields import BaseField
from odmantic.field import ODMFieldInfo
from opinionated_mixins.contrib import (
    mongoengine as me_contrib,
)
from opinionated_mixins.contrib import (
    odmantic as od_contrib,
)
from opinionated_mixins.contrib import (
    sqlalchemy as sa_contrib,
)
from opinionated_mixins.contrib import (
    sqlmodel as sm_contrib,
)
from sqlalchemy import Column

MIXIN_NAMES = [
    "Activity",
    "Announcement",
    "CreatedAt",
    "Feedback",
    "IsActive",
    "Lead",
    "Notification",
    "Person",
    "Template",
    "UpdatedAt",
    "User",
]

SQL_ONLY_MIXIN_NAMES = ["IntegerID", "UUIDID"]

REFERENCE_FRAMEWORK = "sqlalchemy"


def _isinstance_extractor(field_type: type) -> Callable[[type], set[str]]:
    """Create an extractor that finds fields by isinstance check on __dict__."""

    def extract(mixin_cls: type) -> set[str]:
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, field_type)
        }

    return extract


FRAMEWORKS: dict[str, tuple[object, Callable[[type], set[str]]]] = {
    "sqlalchemy": (sa_contrib, _isinstance_extractor(Column)),
    "sqlmodel": (sm_contrib, _isinstance_extractor(Column)),
    "mongoengine": (me_contrib, _isinstance_extractor(BaseField)),
    "odmantic": (od_contrib, _isinstance_extractor(ODMFieldInfo)),
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
        missing = reference_fields - fields
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


@pytest.mark.parametrize("mixin_name", SQL_ONLY_MIXIN_NAMES)
def test_sql_only_mixins_exported(mixin_name: str) -> None:
    """SQL-only mixins must be exported by sqlalchemy and sqlmodel."""
    for fw_name in ("sqlalchemy", "sqlmodel"):
        module = FRAMEWORKS[fw_name][0]
        assert hasattr(module, mixin_name), f"{fw_name} does not export {mixin_name}"


@pytest.mark.parametrize("mixin_name", SQL_ONLY_MIXIN_NAMES)
def test_sql_only_mixins_not_in_nosql(mixin_name: str) -> None:
    """SQL-only mixins must NOT be exported by mongoengine or odmantic."""
    for fw_name in ("mongoengine", "odmantic"):
        module = FRAMEWORKS[fw_name][0]
        assert not hasattr(module, mixin_name), (
            f"{fw_name} should not export {mixin_name}"
        )
