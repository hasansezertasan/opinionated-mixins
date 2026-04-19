from opinionated_mixins.contrib.wtforms import Announcement
from opinionated_mixins.enums import AnnouncementCategory
from wtforms import Form


class AnnouncementForm(Announcement, Form):  # type: ignore[misc]
    pass


class TestWTFormsAnnouncement:
    def test_has_fields(self) -> None:
        form = AnnouncementForm()
        assert "title" in form._fields
        assert "content" in form._fields
        assert "category" in form._fields

    def test_category_choices(self) -> None:
        form = AnnouncementForm()
        choice_values = [c[0] for c in form.category.choices]
        expected = [c.value for c in AnnouncementCategory]
        assert choice_values == expected

    def test_category_default(self) -> None:
        form = AnnouncementForm()
        assert form.category.default == AnnouncementCategory.GENERAL.value

    def test_valid_submission(self) -> None:
        form = AnnouncementForm(
            data={
                "title": "Test",
                "content": "Hello world",
                "category": "general",
            },
        )
        assert form.validate()
