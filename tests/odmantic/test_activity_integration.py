"""Integration tests for ODMantic Activity mixin."""

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import Activity
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=False,
)


class MyActivity(Activity, Model):
    """Test model composing Activity with Model."""

    model_config = {"collection": "test_activities"}


class TestActivityIntegration:
    """Test Activity mixin composition, instantiation, and roundtrip."""

    async def test_create_with_required_fields(self, mock_engine) -> None:
        obj = MyActivity(
            verb="commented",
            actor_type="User",
            actor_id="42",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyActivity)
        assert loaded is not None
        assert loaded.verb == "commented"
        assert loaded.actor_type == "User"
        assert loaded.actor_id == "42"
        assert loaded.public is True

    async def test_optional_fields_null_by_default(self, mock_engine) -> None:
        obj = MyActivity(
            verb="deployed",
            actor_type="System",
            actor_id="system",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyActivity)
        assert loaded is not None
        assert loaded.description is None
        assert loaded.target_type is None
        assert loaded.target_id is None
        assert loaded.action_object_type is None
        assert loaded.action_object_id is None

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyActivity(
            verb="commented",
            description="Alice commented on a pull request",
            data={"comment_id": "5"},
            actor_type="User",
            actor_id="42",
            target_type="PullRequest",
            target_id="99",
            action_object_type="Comment",
            action_object_id="5",
            public=False,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyActivity)
        assert loaded.verb == "commented"
        assert loaded.description == "Alice commented on a pull request"
        assert loaded.data == {"comment_id": "5"}
        assert loaded.actor_type == "User"
        assert loaded.actor_id == "42"
        assert loaded.target_type == "PullRequest"
        assert loaded.target_id == "99"
        assert loaded.action_object_type == "Comment"
        assert loaded.action_object_id == "5"
        assert loaded.public is False

    async def test_created_at_set_on_insert(self, mock_engine) -> None:
        obj = MyActivity(
            verb="merged",
            actor_type="User",
            actor_id="1",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyActivity)
        assert loaded.created_at is not None
