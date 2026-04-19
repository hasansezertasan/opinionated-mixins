import dataclasses
import datetime

from opinionated_mixins.contrib.dataclasses import User


class TestDataclassesUser:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(User)

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

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(User)}
        expected = {
            "username",
            "hashed_password",
            "email",
            "date_email_verified",
        }
        assert fields == expected
