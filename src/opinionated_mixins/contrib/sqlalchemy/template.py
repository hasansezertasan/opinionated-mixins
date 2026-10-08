from opinionated_mixins.enums import TemplateFormat, TemplateType

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Template"]


@declarative_mixin
class Template:
    """Template mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``name``: index recommended for template lookups by name (or unique index
      if names are unique per scope).
    - ``type``: index recommended if filtering templates by type.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyTemplate(Template, Base):
                __tablename__ = "templates"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_templates_name", "name"),)
    """

    __abstract__ = True

    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    format = Column(Enum(TemplateFormat), nullable=False, default=TemplateFormat.PLAIN)
    type = Column(Enum(TemplateType), nullable=False, default=TemplateType.OTHER)
