import pytest
from opinionated_mixins.contrib.pydantic import Announcement, Person, User
from opinionated_mixins.enums import AnnouncementCategory
from pydantic import BaseModel, ValidationError


class CombinedModel(User, Person, Announcement, BaseModel):
    pass


class TestPydanticMixinComposition:
    def test_all_fields_available(self) -> None:
        obj = CombinedModel(
            username="jdoe",
            hashed_password="hashed123",
            first_name="John",
            last_name="Doe",
            title="Test announcement",
            content="Hello world",
        )
        assert obj.username == "jdoe"
        assert obj.hashed_password == "hashed123"
        assert obj.first_name == "John"
        assert obj.last_name == "Doe"
        assert obj.title == "Test announcement"
        assert obj.content == "Hello world"
        assert obj.category == AnnouncementCategory.GENERAL

    def test_validation_runs_across_all_mixins(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            CombinedModel(
                username="",
                hashed_password="hashed123",
                first_name="",
                last_name="Doe",
                title="",
                content="Body",
            )
        errors = exc_info.value.errors()
        fields_with_errors = {e["loc"][0] for e in errors}
        assert "username" in fields_with_errors
        assert "first_name" in fields_with_errors
        assert "title" in fields_with_errors

    def test_optional_fields_from_multiple_mixins(self) -> None:
        obj = CombinedModel(
            username="jdoe",
            hashed_password="hashed123",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone_number="+1234567890",
            country="US",
            title="Update",
            content="New feature",
            category=AnnouncementCategory.UPDATE,
        )
        assert obj.email == "jane@example.com"
        assert obj.phone_number == "+1234567890"
        assert obj.country == "US"
        assert obj.category == AnnouncementCategory.UPDATE
