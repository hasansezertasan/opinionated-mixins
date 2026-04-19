import dataclasses

from opinionated_mixins.contrib.dataclasses import Announcement
from opinionated_mixins.enums import AnnouncementCategory


class TestDataclassesAnnouncement:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(Announcement)

    def test_create_with_defaults(self) -> None:
        obj = Announcement(title="Test", content="Hello world")
        assert obj.title == "Test"
        assert obj.content == "Hello world"
        assert obj.category == AnnouncementCategory.GENERAL

    def test_create_with_category(self) -> None:
        obj = Announcement(
            title="Event",
            content="Join us",
            category=AnnouncementCategory.EVENT,
        )
        assert obj.category == AnnouncementCategory.EVENT

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(Announcement)}
        assert fields == {"title", "content", "category"}
