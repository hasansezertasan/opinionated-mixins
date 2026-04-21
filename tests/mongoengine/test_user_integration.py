"""Integration tests for MongoEngine User mixin."""

import datetime

from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import User


class MyUser(User, Document):
    """Test model composing User with Document."""

    meta = {"collection": "test_users"}


class TestUserIntegration:
    """Test User mixin composition, instantiation, and roundtrip."""

    def test_create_with_required_fields(self) -> None:
        obj = MyUser(username="alice", hashed_password="hashed123")
        obj.save()
        loaded = MyUser.objects.first()
        assert loaded is not None
        assert loaded.username == "alice"
        assert loaded.hashed_password == "hashed123"
        assert loaded.email is None
        assert loaded.date_email_verified is None

    def test_create_with_all_fields(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        obj = MyUser(
            username="bob",
            hashed_password="hashed456",
            email="bob@example.com",
            date_email_verified=now,
        )
        obj.save()
        loaded = MyUser.objects.first()
        assert loaded.email == "bob@example.com"
        assert loaded.date_email_verified is not None

    def test_roundtrip_preserves_all_fields(self) -> None:
        obj = MyUser(
            username="charlie",
            hashed_password="hashed789",
            email="charlie@example.com",
        )
        obj.save()
        loaded = MyUser.objects.first()
        assert loaded.username == "charlie"
        assert loaded.hashed_password == "hashed789"
        assert loaded.email == "charlie@example.com"
