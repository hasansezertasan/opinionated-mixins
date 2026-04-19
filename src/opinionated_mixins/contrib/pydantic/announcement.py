# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import AnnouncementCategory

from pydantic import BaseModel, Field


class Announcement(BaseModel):
    """Announcement mixin for Pydantic models."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: AnnouncementCategory = Field(default=AnnouncementCategory.GENERAL)
