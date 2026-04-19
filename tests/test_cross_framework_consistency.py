"""Cross-framework field consistency tests.

Verifies that every contrib module exposes the same field names for each mixin,
catching drift where one framework uses a different name than the others.

See: https://github.com/hasansezertasan/opinionated-mixins/issues/32
"""

from __future__ import annotations

import dataclasses

import pytest
from mongoengine.base.fields import BaseField
from odmantic.field import ODMFieldInfo
from pydantic.fields import FieldInfo as PydanticFieldInfo
from sqlalchemy import Column
from wtforms.fields.core import UnboundField as WTUnboundField

from opinionated_mixins.contrib import (
    dataclasses as dc_contrib,
    mongoengine as me_contrib,
    odmantic as od_contrib,
    pydantic as pd_contrib,
    sqlalchemy as sa_contrib,
    sqlmodel as sm_contrib,
    wtforms as wt_contrib,
)

MIXIN_NAMES = ["Announcement", "Feedback", "Lead", "Person", "Template", "User"]

# Fields intentionally excluded from specific frameworks.
# Key: (framework, mixin), Value: set of field names to ignore.
EXPECTED_EXCLUSIONS: dict[tuple[str, str], set[str]] = {
    # WTForms collects raw input; password hashing is app-level concern.
    ("wtforms", "User"): {"hashed_password"},
}

FRAMEWORKS = {
    "pydantic": pd_contrib,
    "sqlalchemy": sa_contrib,
    "sqlmodel": sm_contrib,
    "mongoengine": me_contrib,
    "odmantic": od_contrib,
    "wtforms": wt_contrib,
    "dataclasses": dc_contrib,
}


def _get_field_names(framework: str, mixin_cls: type) -> set[str]:
    """Extract field names from a mixin class using framework-specific introspection."""
    if framework == "dataclasses":
        return {f.name for f in dataclasses.fields(mixin_cls)}

    if framework in ("pydantic", "odmantic"):
        field_type = ODMFieldInfo if framework == "odmantic" else PydanticFieldInfo
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, field_type)
        }

    if framework in ("sqlalchemy", "sqlmodel"):
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, Column)
        }

    if framework == "mongoengine":
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, BaseField)
        }

    if framework == "wtforms":
        return {
            name
            for name, value in mixin_cls.__dict__.items()
            if isinstance(value, WTUnboundField)
        }

    msg = f"Unknown framework: {framework}"
    raise ValueError(msg)


@pytest.mark.parametrize("mixin_name", MIXIN_NAMES)
def test_all_frameworks_have_same_fields(mixin_name: str) -> None:
    """Each mixin must expose identical field names across all frameworks."""
    fields_by_framework: dict[str, set[str]] = {}
    for fw_name, module in FRAMEWORKS.items():
        mixin_cls = getattr(module, mixin_name)
        fields_by_framework[fw_name] = _get_field_names(fw_name, mixin_cls)

    reference_fw = "pydantic"
    reference_fields = fields_by_framework[reference_fw]

    for fw_name, fields in fields_by_framework.items():
        if fw_name == reference_fw:
            continue
        excluded = EXPECTED_EXCLUSIONS.get((fw_name, mixin_name), set())
        missing = reference_fields - fields - excluded
        extra = fields - reference_fields
        assert not missing and not extra, (
            f"{mixin_name}: {fw_name} vs {reference_fw} mismatch. "
            f"Missing: {missing or 'none'}. Extra: {extra or 'none'}."
        )


@pytest.mark.parametrize("mixin_name", MIXIN_NAMES)
def test_all_frameworks_export_mixin(mixin_name: str) -> None:
    """Every framework module must export every mixin."""
    for fw_name, module in FRAMEWORKS.items():
        assert hasattr(module, mixin_name), (
            f"{fw_name} does not export {mixin_name}"
        )
