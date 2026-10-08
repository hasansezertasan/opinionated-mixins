from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["IsActive"]


class IsActive(metaclass=ODManticMixinMetaclass):
    """IsActive mixin for ODMantic models."""

    is_active: bool = Field(default=True)
