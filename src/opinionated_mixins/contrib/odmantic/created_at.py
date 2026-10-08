import datetime

from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["CreatedAt"]


class CreatedAt(metaclass=ODManticMixinMetaclass):
    """CreatedAt mixin for ODMantic models."""

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
