from opinionated_mixins.enums import AnnouncementCategory
from sqlalchemy import Text
from sqlmodel import Field


__all__ = ["Announcement"]


class Announcement:
    """Announcement mixin for SQLModel models.

    Indexing recommendations:
    - ``title``: index recommended if searching or ordering announcements by title.
    - ``category``: index recommended if filtering announcements by category.
    """

    title: str = Field(max_length=255)
    content: str = Field(sa_type=Text)
    category: AnnouncementCategory = Field(default=AnnouncementCategory.GENERAL)
