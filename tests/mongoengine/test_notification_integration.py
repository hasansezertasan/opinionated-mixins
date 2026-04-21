"""Integration tests for MongoEngine Notification mixin."""

import datetime

from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import Notification
from opinionated_mixins.enums import NotificationLevel


class MyNotification(Notification, Document):
    """Test model composing Notification with Document."""

    meta = {"collection": "test_notifications"}


class TestNotificationIntegration:
    """Test Notification mixin composition, instantiation, and roundtrip."""

    def test_create_with_required_fields(self) -> None:
        obj = MyNotification(
            notification_type="comment.reply",
            title="Someone replied",
        )
        obj.save()
        loaded = MyNotification.objects.first()
        assert loaded is not None
        assert loaded.notification_type == "comment.reply"
        assert loaded.title == "Someone replied"
        assert loaded.level == NotificationLevel.INFO.value

    def test_create_with_explicit_level(self) -> None:
        obj = MyNotification(
            notification_type="order.shipped",
            title="Order shipped",
            level=NotificationLevel.SUCCESS.value,
        )
        obj.save()
        loaded = MyNotification.objects.first()
        assert loaded.level == NotificationLevel.SUCCESS.value

    def test_optional_fields_null_by_default(self) -> None:
        obj = MyNotification(
            notification_type="system.alert",
            title="Alert",
        )
        obj.save()
        loaded = MyNotification.objects.first()
        assert loaded is not None
        assert loaded.description is None
        assert loaded.actor_type is None
        assert loaded.actor_id is None
        assert loaded.action_url is None
        assert loaded.group_key is None
        assert loaded.seen_at is None
        assert loaded.read_at is None
        assert loaded.archived_at is None

    def test_roundtrip_preserves_all_fields(self) -> None:
        now = datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        obj = MyNotification(
            notification_type="order.shipped",
            level=NotificationLevel.SUCCESS.value,
            title="Order shipped",
            description="Your order is on the way",
            actor_type="User",
            actor_id="42",
            action_url="https://example.com/orders/123",
            group_key="order.123",
            seen_at=now,
            read_at=now,
        )
        obj.save()
        loaded = MyNotification.objects.first()
        assert loaded.notification_type == "order.shipped"
        assert loaded.level == NotificationLevel.SUCCESS.value
        assert loaded.title == "Order shipped"
        assert loaded.description == "Your order is on the way"
        assert loaded.actor_type == "User"
        assert loaded.actor_id == "42"
        assert loaded.group_key == "order.123"
