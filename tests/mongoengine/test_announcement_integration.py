"""Integration tests for MongoEngine Announcement mixin."""

from mongoengine import Document

from opinionated_mixins.contrib.mongoengine import Announcement
from opinionated_mixins.enums import AnnouncementCategory


class MyAnnouncement(Announcement, Document):
    """Test model composing Announcement with Document."""

    meta = {"collection": "test_announcements"}


class TestAnnouncementIntegration:
    """Test Announcement mixin composition, instantiation, and roundtrip."""

    def test_create_with_defaults(self) -> None:
        obj = MyAnnouncement(title="Test", content="Hello world")
        obj.save()
        loaded = MyAnnouncement.objects.first()
        assert loaded is not None
        assert loaded.title == "Test"
        assert loaded.content == "Hello world"
        assert loaded.category == AnnouncementCategory.GENERAL.value

    def test_create_with_explicit_category(self) -> None:
        obj = MyAnnouncement(
            title="Downtime",
            content="Scheduled maintenance",
            category=AnnouncementCategory.MAINTENANCE.value,
        )
        obj.save()
        loaded = MyAnnouncement.objects.first()
        assert loaded.category == AnnouncementCategory.MAINTENANCE.value

    def test_roundtrip_preserves_all_fields(self) -> None:
        obj = MyAnnouncement(
            title="Alert",
            content="System update",
            category=AnnouncementCategory.WARNING.value,
        )
        obj.save()
        loaded = MyAnnouncement.objects.first()
        assert loaded.title == "Alert"
        assert loaded.content == "System update"
        assert loaded.category == AnnouncementCategory.WARNING.value
