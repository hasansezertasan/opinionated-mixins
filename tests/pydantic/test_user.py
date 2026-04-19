import datetime

import pytest
from opinionated_mixins.contrib.pydantic import User
from pydantic import ValidationError


class TestPydanticUser:
    def test_create_with_required_only(self) -> None:
        obj = User(username="janedoe", hashed_password="hashed123")
        assert obj.username == "janedoe"
        assert obj.hashed_password == "hashed123"
        assert obj.email is None
        assert obj.date_email_verified is None

    def test_create_with_all_fields(self) -> None:
        now = datetime.datetime(2024, 1, 15, 12, 0, 0)
        obj = User(
            username="janedoe",
            hashed_password="hashed123",
            email="jane@example.com",
            date_email_verified=now,
        )
        assert obj.email == "jane@example.com"
        assert obj.date_email_verified == now

    def test_username_required(self) -> None:
        with pytest.raises(ValidationError):
            User(hashed_password="hashed123")  # type: ignore[call-arg]

    def test_hashed_password_required(self) -> None:
        with pytest.raises(ValidationError):
            User(username="janedoe")  # type: ignore[call-arg]

    def test_empty_username_rejected(self) -> None:
        with pytest.raises(ValidationError):
            User(username="", hashed_password="hashed123")

    def test_username_max_length(self) -> None:
        with pytest.raises(ValidationError):
            User(username="x" * 256, hashed_password="hashed123")

    def test_empty_hashed_password_rejected(self) -> None:
        with pytest.raises(ValidationError):
            User(username="janedoe", hashed_password="")

    def test_email_max_length(self) -> None:
        with pytest.raises(ValidationError):
            User(username="janedoe", hashed_password="hashed123", email="x" * 255)
