from opinionated_mixins.contrib.wtforms import User
from wtforms import Form


class UserForm(User, Form):  # type: ignore[misc]
    pass


USER_FIELDS = {
    "username",
    "password",
    "email",
    "date_email_verified",
}


class TestWTFormsUser:
    def test_has_fields(self) -> None:
        form = UserForm()
        for field_name in USER_FIELDS:
            assert field_name in form._fields, f"Missing field: {field_name}"

    def test_valid_submission_required_only(self) -> None:
        form = UserForm(
            data={
                "username": "janedoe",
                "password": "secret123",
            },
        )
        assert form.validate()

    def test_valid_submission_all_fields(self) -> None:
        form = UserForm(
            data={
                "username": "janedoe",
                "password": "secret123",
                "email": "jane@example.com",
                "date_email_verified": "2024-01-15 12:00:00",
            },
        )
        assert form.validate()

    def test_missing_username_invalid(self) -> None:
        form = UserForm(
            data={
                "password": "secret123",
            },
        )
        assert not form.validate()
        assert "username" in form.errors

    def test_missing_password_invalid(self) -> None:
        form = UserForm(
            data={
                "username": "janedoe",
            },
        )
        assert not form.validate()
        assert "password" in form.errors
