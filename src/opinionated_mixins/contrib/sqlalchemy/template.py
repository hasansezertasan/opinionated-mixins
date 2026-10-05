from opinionated_mixins.enums import TemplateFormat, TemplateType

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Template:
    """Template mixin for SQLAlchemy models."""

    __abstract__ = True

    name = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    format = Column(Enum(TemplateFormat), nullable=False, default=TemplateFormat.PLAIN)
    type = Column(Enum(TemplateType), nullable=False, default=TemplateType.OTHER)
