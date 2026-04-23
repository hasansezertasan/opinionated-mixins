import datetime
from typing import Any, ClassVar

from opinionated_mixins.enums import NotificationLevel

from mongoengine import DateTimeField, DictField, StringField


class Notification:
    """Notification mixin for MongoEngine documents.

    Tracks per-recipient notification state: type, severity, read/seen status,
    and metadata about the triggering action.

    Note: Does not include recipient reference. Each contrib implementation
    should add recipient using MongoEngine's ReferenceField or similar.
    """

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    notification_type = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text=(
            "Dot-notation type identifier (e.g. 'comment.reply', 'order.shipped')"
        ),
    )
    level = StringField(
        required=True,
        default=NotificationLevel.INFO.value,
        choices=[level.value for level in NotificationLevel],
        index=True,
        help_text="Severity/criticality level of notification",
    )
    title = StringField(
        required=True,
        max_length=255,
        help_text="Short human-readable title",
    )
    description = StringField(
        help_text="Longer human-readable body",
    )
    data = DictField(
        help_text="Arbitrary JSON payload for extra context",
    )
    actor_type = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text="Polymorphic type of entity that triggered notification",
    )
    actor_id = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text="Polymorphic ID of entity that triggered notification",
    )
    action_url = StringField(
        max_length=2048,
        help_text="Click-through URL for the notification",
    )
    group_key = StringField(
        max_length=255,
        index=True,
        help_text="Grouping key for batching similar notifications",
    )
    seen_at = DateTimeField(
        index=True,
        help_text="When notification appeared in user's feed; None = unseen",
    )
    read_at = DateTimeField(
        index=True,
        help_text="When user clicked/opened notification; None = unread",
    )
    archived_at = DateTimeField(
        index=True,
        help_text="When user archived/dismissed notification; None = not archived",
    )
    created_at = DateTimeField(
        required=True,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        help_text="When notification was created",
    )
