from opinionated_mixins.contrib.odmantic import User


class TestODManticUser:
    def test_has_expected_annotations(self) -> None:
        annotations = User.__annotations__
        assert "username" in annotations
        assert "hashed_password" in annotations
        assert "email" in annotations
        assert "date_email_verified" in annotations

    def test_optional_fields_default_none(self) -> None:
        for field_name in (
            "email",
            "date_email_verified",
        ):
            field_info = getattr(User, field_name).pydantic_field_info
            assert field_info.default is None, f"{field_name} should default to None"
