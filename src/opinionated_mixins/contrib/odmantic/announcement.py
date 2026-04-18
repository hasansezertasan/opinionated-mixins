# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from odmantic import Field
from opinionated_mixins.enums import AnnouncementCategory


class Announcement:
    """Announcement mixin for ODMantic models."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: AnnouncementCategory = Field(default=AnnouncementCategory.GENERAL)
