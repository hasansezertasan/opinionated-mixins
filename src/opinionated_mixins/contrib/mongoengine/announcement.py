# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from typing import Any, ClassVar, Dict

from mongoengine import StringField
from opinionated_mixins.enums import AnnouncementCategory


class Announcement:
    """Announcement mixin for MongoEngine documents."""

    meta: ClassVar[Dict[str, Any]] = {"allow_inheritance": True}

    title = StringField(required=True, max_length=255)
    content = StringField(required=True)
    category = StringField(
        required=True,
        default=AnnouncementCategory.GENERAL.value,
        choices=[c.value for c in AnnouncementCategory],
    )
