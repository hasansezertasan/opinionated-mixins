from opinionated_mixins.enums import AnnouncementCategory

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Announcement:
    """Announcement mixin for SQLAlchemy models."""

    __abstract__ = True

    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(
        Enum(AnnouncementCategory), nullable=False, default=AnnouncementCategory.GENERAL,
    )
