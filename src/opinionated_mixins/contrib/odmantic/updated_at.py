import datetime

from odmantic import Field
from pydantic import field_validator

from ._base import ODManticMixinMetaclass, utc_datetime

__all__ = ["UpdatedAt"]


class UpdatedAt(metaclass=ODManticMixinMetaclass):
    """UpdatedAt mixin for ODMantic models."""

    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    _restore_updated_at_utc = field_validator("updated_at", mode="before")(utc_datetime)
