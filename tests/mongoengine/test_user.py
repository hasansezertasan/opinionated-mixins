from opinionated_mixins.contrib.mongoengine import User


class TestMongoEngineUser:
    def test_has_username_field(self) -> None:
        assert hasattr(User, "username")
        assert User.username.required is True
        assert User.username.max_length == 255
        assert User.username.unique is True

    def test_has_hashed_password_field(self) -> None:
        assert hasattr(User, "hashed_password")
        assert User.hashed_password.required is True
        assert User.hashed_password.max_length == 1024

    def test_has_email_field(self) -> None:
        assert hasattr(User, "email")
        assert User.email.required is False
        assert User.email.max_length == 254
        assert User.email.unique is True

    def test_has_date_email_verified_field(self) -> None:
        assert hasattr(User, "date_email_verified")
        assert User.date_email_verified.required is False
