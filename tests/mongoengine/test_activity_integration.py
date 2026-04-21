"""Integration tests for MongoEngine Activity mixin."""

import datetime

from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import Activity


class MyActivity(Activity, Document):
    """Test model composing Activity with Document."""

    meta = {"collection": "test_activities"}


class TestActivityIntegration:
    """Test Activity mixin composition, instantiation, and roundtrip."""

    def test_create_with_required_fields(self) -> None:
        obj = MyActivity(
            verb="commented",
            actor_type="User",
            actor_id="42",
        )
        obj.save()
        loaded = MyActivity.objects.first()
        assert loaded is not None
        assert loaded.verb == "commented"
        assert loaded.actor_type == "User"
        assert loaded.actor_id == "42"
        assert loaded.public is True

    def test_optional_fields_null_by_default(self) -> None:
        obj = MyActivity(
            verb="deployed",
            actor_type="System",
            actor_id="system",
        )
        obj.save()
        loaded = MyActivity.objects.first()
        assert loaded is not None
        assert loaded.description is None
        assert loaded.target_type is None
        assert loaded.target_id is None
        assert loaded.action_object_type is None
        assert loaded.action_object_id is None

    def test_public_defaults_true(self) -> None:
        obj = MyActivity(
            verb="created",
            actor_type="User",
            actor_id="1",
        )
        obj.save()
        loaded = MyActivity.objects.first()
        assert loaded is not None
        assert loaded.public is True

    def test_roundtrip_preserves_all_fields(self) -> None:
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
        obj.save()
        loaded = MyActivity.objects.first()
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

    def test_created_at_set_on_insert(self) -> None:
        obj = MyActivity(
            verb="merged",
            actor_type="User",
            actor_id="1",
        )
        obj.save()
        loaded = MyActivity.objects.first()
        assert loaded.created_at is not None
        assert isinstance(loaded.created_at, datetime.datetime)
