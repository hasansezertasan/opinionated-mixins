from opinionated_mixins.enums import TemplateFormat, TemplateType

from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["Template"]


class Template(metaclass=ODManticMixinMetaclass):
    """Template mixin for ODMantic models."""

    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    format: TemplateFormat = Field(default=TemplateFormat.PLAIN)
    type: TemplateType = Field(default=TemplateType.OTHER)
