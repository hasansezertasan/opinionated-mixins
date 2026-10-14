from opinionated_mixins.enums import TemplateFormat, TemplateType
from sqlalchemy import Text
from sqlmodel import Field


__all__ = ["Template"]


class Template:
    """Template mixin for SQLModel models."""

    name: str = Field(max_length=255)
    content: str = Field(sa_type=Text)
    format: TemplateFormat = Field(default=TemplateFormat.PLAIN)
    type: TemplateType = Field(default=TemplateType.OTHER)
