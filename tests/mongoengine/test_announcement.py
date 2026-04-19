from opinionated_mixins.contrib.mongoengine import Announcement
from opinionated_mixins.enums import AnnouncementCategory


class TestMongoEngineAnnouncement:
    def test_has_title_field(self) -> None:
        assert hasattr(Announcement, "title")
        assert Announcement.title.required is True
        assert Announcement.title.max_length == 255

    def test_has_content_field(self) -> None:
        assert hasattr(Announcement, "content")
        assert Announcement.content.required is True

    def test_has_category_field(self) -> None:
        assert hasattr(Announcement, "category")
        assert Announcement.category.required is True
        assert Announcement.category.default == AnnouncementCategory.GENERAL.value

    def test_category_choices(self) -> None:
        choices = Announcement.category.choices
        expected = [c.value for c in AnnouncementCategory]
        assert choices == expected
