from typing import Any, ClassVar

from opinionated_mixins.enums import AnnouncementCategory

from mongoengine import StringField


class Announcement:
    """Announcement mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    title = StringField(required=True, max_length=255)
    content = StringField(required=True)
    category = StringField(
        required=True,
        default=AnnouncementCategory.GENERAL.value,
        choices=[c.value for c in AnnouncementCategory],
    )
