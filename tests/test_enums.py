# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import AnnouncementCategory


class TestAnnouncementCategory:
    def test_values(self) -> None:
        expected = [
            "general",
            "info",
            "warning",
            "success",
            "error",
            "maintenance",
            "update",
            "event",
        ]
        assert [c.value for c in AnnouncementCategory] == expected

    def test_str_mixin(self) -> None:
        assert AnnouncementCategory.GENERAL == "general"
        assert isinstance(AnnouncementCategory.INFO, str)

    def test_lookup_by_value(self) -> None:
        assert AnnouncementCategory("warning") is AnnouncementCategory.WARNING
