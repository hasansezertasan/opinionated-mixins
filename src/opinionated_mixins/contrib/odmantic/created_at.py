import datetime as dt

from odmantic import Field
from pydantic import field_validator

from ._base import ODManticMixinMetaclass, utc_datetime

__all__ = ["CreatedAt"]


class CreatedAt(metaclass=ODManticMixinMetaclass):
    """CreatedAt mixin for ODMantic models."""

    created_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )

    _restore_created_at_utc = field_validator("created_at", mode="before")(utc_datetime)
