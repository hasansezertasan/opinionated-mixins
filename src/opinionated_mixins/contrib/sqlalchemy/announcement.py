from opinionated_mixins.enums import AnnouncementCategory

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Announcement"]


@declarative_mixin
class Announcement:
    """Announcement mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``title``: index recommended if searching or ordering announcements by title.
    - ``category``: index recommended if filtering announcements by category.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyAnnouncement(Announcement, Base):
                __tablename__ = "announcements"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_announcements_title", "title"),)
    """

    __abstract__ = True

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(
        Enum(AnnouncementCategory), nullable=False, default=AnnouncementCategory.GENERAL
    )
