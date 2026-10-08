import datetime

from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["UpdatedAt"]


class UpdatedAt(metaclass=ODManticMixinMetaclass):
    """UpdatedAt mixin for ODMantic models."""

    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
