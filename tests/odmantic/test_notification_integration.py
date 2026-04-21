"""Integration tests for ODMantic Notification mixin."""

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import Notification
from opinionated_mixins.enums import NotificationLevel
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=False,
)


class MyNotification(Notification, Model):
    """Test model composing Notification with Model."""

    model_config = {"collection": "test_notifications"}


class TestNotificationIntegration:
    """Test Notification mixin composition, instantiation, and roundtrip."""

    async def test_create_with_required_fields(self, mock_engine) -> None:
        obj = MyNotification(
            notification_type="comment.reply",
            title="Someone replied",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyNotification)
        assert loaded is not None
        assert loaded.notification_type == "comment.reply"
        assert loaded.title == "Someone replied"
        assert loaded.level == NotificationLevel.INFO

    async def test_create_with_explicit_level(self, mock_engine) -> None:
        obj = MyNotification(
            notification_type="order.shipped",
            title="Order shipped",
            level=NotificationLevel.SUCCESS,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyNotification)
        assert loaded.level == NotificationLevel.SUCCESS

    async def test_optional_fields_null_by_default(self, mock_engine) -> None:
        obj = MyNotification(
            notification_type="system.alert",
            title="Alert",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyNotification)
        assert loaded is not None
        assert loaded.description is None
        assert loaded.actor_type is None
        assert loaded.actor_id is None
        assert loaded.seen_at is None
        assert loaded.read_at is None
        assert loaded.archived_at is None

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyNotification(
            notification_type="order.shipped",
            level=NotificationLevel.SUCCESS,
            title="Order shipped",
            description="Your order is on the way",
            actor_type="User",
            actor_id="42",
            action_url="https://example.com/orders/123",
            group_key="order.123",
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyNotification)
        assert loaded.notification_type == "order.shipped"
        assert loaded.level == NotificationLevel.SUCCESS
        assert loaded.title == "Order shipped"
        assert loaded.description == "Your order is on the way"
        assert loaded.actor_type == "User"
        assert loaded.actor_id == "42"
        assert loaded.group_key == "order.123"
