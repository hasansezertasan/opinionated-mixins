# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import pytest
from pydantic import ValidationError

from opinionated_mixins.contrib.pydantic import Announcement
from opinionated_mixins.enums import AnnouncementCategory


class TestPydanticAnnouncement:
    def test_create_with_defaults(self) -> None:
        obj = Announcement(title="Test", content="Hello world")
        assert obj.title == "Test"
        assert obj.content == "Hello world"
        assert obj.category == AnnouncementCategory.GENERAL

    def test_create_with_category(self) -> None:
        obj = Announcement(
            title="Update",
            content="New feature",
            category=AnnouncementCategory.UPDATE,
        )
        assert obj.category == AnnouncementCategory.UPDATE

    def test_title_required(self) -> None:
        with pytest.raises(ValidationError):
            Announcement(content="No title")  # type: ignore[call-arg]

    def test_content_required(self) -> None:
        with pytest.raises(ValidationError):
            Announcement(title="No content")  # type: ignore[call-arg]

    def test_empty_title_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Announcement(title="", content="Body")

    def test_title_max_length(self) -> None:
        with pytest.raises(ValidationError):
            Announcement(title="x" * 256, content="Body")

    def test_category_from_string(self) -> None:
        obj = Announcement(title="Test", content="Body", category="warning")  # type: ignore[arg-type]
        assert obj.category == AnnouncementCategory.WARNING

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Announcement(title="Test", content="Body", category="invalid")  # type: ignore[arg-type]
