# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import AnnouncementCategory, TemplateFormat, TemplateType


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


class TestTemplateFormat:
    def test_values(self) -> None:
        expected = ["plain", "html", "markdown"]
        assert [c.value for c in TemplateFormat] == expected

    def test_str_mixin(self) -> None:
        assert TemplateFormat.PLAIN == "plain"
        assert isinstance(TemplateFormat.HTML, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateFormat("html") is TemplateFormat.HTML


class TestTemplateType:
    def test_values(self) -> None:
        expected = ["email", "sms", "push", "other"]
        assert [c.value for c in TemplateType] == expected

    def test_str_mixin(self) -> None:
        assert TemplateType.EMAIL == "email"
        assert isinstance(TemplateType.SMS, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateType("push") is TemplateType.PUSH
