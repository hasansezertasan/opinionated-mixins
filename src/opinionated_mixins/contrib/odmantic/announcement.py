from opinionated_mixins.enums import AnnouncementCategory

from odmantic import Field


class Announcement:
    """Announcement mixin for ODMantic models."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: AnnouncementCategory = Field(default=AnnouncementCategory.GENERAL)
