# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.odmantic import Announcement
from opinionated_mixins.enums import AnnouncementCategory


class TestODManticAnnouncement:
    def test_has_expected_annotations(self) -> None:
        annotations = Announcement.__annotations__
        assert "title" in annotations
        assert "content" in annotations
        assert "category" in annotations

    def test_category_default(self) -> None:
        assert Announcement.category.pydantic_field_info.default == AnnouncementCategory.GENERAL
