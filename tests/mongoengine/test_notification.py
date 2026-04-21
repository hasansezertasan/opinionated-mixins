from opinionated_mixins.contrib.mongoengine import Notification
from opinionated_mixins.enums import NotificationLevel


class TestMongoEngineNotification:
    def test_has_notification_type_field(self) -> None:
        assert hasattr(Notification, "notification_type")
        assert Notification.notification_type.required is True
        assert Notification.notification_type.max_length == 255

    def test_has_level_field(self) -> None:
        assert hasattr(Notification, "level")
        assert Notification.level.required is True
        assert Notification.level.default == NotificationLevel.INFO.value

    def test_level_choices(self) -> None:
        choices = Notification.level.choices
        expected = [level.value for level in NotificationLevel]
        assert choices == expected

    def test_has_title_field(self) -> None:
        assert hasattr(Notification, "title")
        assert Notification.title.required is True
        assert Notification.title.max_length == 255

    def test_has_description_field(self) -> None:
        assert hasattr(Notification, "description")
        assert Notification.description.required is False

    def test_has_data_field(self) -> None:
        assert hasattr(Notification, "data")

    def test_has_actor_fields(self) -> None:
        assert hasattr(Notification, "actor_type")
        assert Notification.actor_type.max_length == 255
        assert hasattr(Notification, "actor_id")
        assert Notification.actor_id.max_length == 255

    def test_has_action_url_field(self) -> None:
        assert hasattr(Notification, "action_url")
        assert Notification.action_url.max_length == 2048

    def test_has_group_key_field(self) -> None:
        assert hasattr(Notification, "group_key")
        assert Notification.group_key.max_length == 255

    def test_has_timestamp_fields(self) -> None:
        assert hasattr(Notification, "seen_at")
        assert hasattr(Notification, "read_at")
        assert hasattr(Notification, "archived_at")
        assert hasattr(Notification, "created_at")
        assert Notification.created_at.required is True
