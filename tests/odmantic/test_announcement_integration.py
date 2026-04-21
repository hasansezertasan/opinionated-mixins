"""Integration tests for ODMantic Announcement mixin."""

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import Announcement
from opinionated_mixins.enums import AnnouncementCategory
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyAnnouncement(Announcement, Model):
    """Test model composing Announcement with Model."""

    model_config = {"collection": "test_announcements"}


class TestAnnouncementIntegration:
    """Test Announcement mixin composition, instantiation, and roundtrip."""

    async def test_create_with_defaults(self, mock_engine) -> None:
        obj = MyAnnouncement(title="Test", content="Hello world")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyAnnouncement)
        assert loaded is not None
        assert loaded.title == "Test"
        assert loaded.content == "Hello world"
        assert loaded.category == AnnouncementCategory.GENERAL

    async def test_create_with_explicit_category(self, mock_engine) -> None:
        obj = MyAnnouncement(
            title="Downtime",
            content="Scheduled maintenance",
            category=AnnouncementCategory.MAINTENANCE,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyAnnouncement)
        assert loaded.category == AnnouncementCategory.MAINTENANCE

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyAnnouncement(
            title="Alert",
            content="System update",
            category=AnnouncementCategory.WARNING,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyAnnouncement)
        assert loaded.title == "Alert"
        assert loaded.content == "System update"
        assert loaded.category == AnnouncementCategory.WARNING
