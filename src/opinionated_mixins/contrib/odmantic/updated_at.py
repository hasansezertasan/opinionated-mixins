import datetime as dt

from odmantic import Field
from pydantic import field_validator

from ._base import ODManticMixinMetaclass, utc_datetime

__all__ = ["UpdatedAt"]


class UpdatedAt(metaclass=ODManticMixinMetaclass):
    """UpdatedAt mixin for ODMantic models."""

    updated_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.UTC))

    _restore_updated_at_utc = field_validator("updated_at", mode="before")(utc_datetime)
