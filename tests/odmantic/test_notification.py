from opinionated_mixins.contrib.odmantic import Notification
from opinionated_mixins.enums import NotificationLevel


class TestODManticNotification:
    def test_has_expected_annotations(self) -> None:
        annotations = Notification.__annotations__
        assert "notification_type" in annotations
        assert "level" in annotations
        assert "title" in annotations
        assert "description" in annotations
        assert "data" in annotations
        assert "actor_type" in annotations
        assert "actor_id" in annotations
        assert "action_url" in annotations
        assert "group_key" in annotations
        assert "seen_at" in annotations
        assert "read_at" in annotations
        assert "archived_at" in annotations
        assert "created_at" in annotations

    def test_level_default(self) -> None:
        assert Notification.level.pydantic_field_info.default == NotificationLevel.INFO
