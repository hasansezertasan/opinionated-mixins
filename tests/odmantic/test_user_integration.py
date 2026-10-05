"""Integration tests for ODMantic User mixin."""

import datetime

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import User
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyUser(User, Model):
    """Test model composing User with Model."""

    model_config = {"collection": "test_users"}


class TestUserIntegration:
    """Test User mixin composition, instantiation, and roundtrip."""

    async def test_create_with_required_fields(self, mock_engine) -> None:
        obj = MyUser(username="alice", hashed_password="hashed123")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyUser)
        assert loaded is not None
        assert loaded.username == "alice"
        assert loaded.hashed_password == "hashed123"
        assert loaded.email is None
        assert loaded.date_email_verified is None

    async def test_create_with_all_fields(self, mock_engine) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        obj = MyUser(
            username="bob",
            hashed_password="hashed456",
            email="bob@example.com",
            date_email_verified=now,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyUser)
        assert loaded.email == "bob@example.com"
        assert loaded.date_email_verified is not None

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyUser(
            username="charlie",
            hashed_password="hashed789",
            email="charlie@example.com",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyUser)
        assert loaded.username == "charlie"
        assert loaded.hashed_password == "hashed789"
        assert loaded.email == "charlie@example.com"
