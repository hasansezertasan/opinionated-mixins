import datetime
from typing import Any

from opinionated_mixins.enums import NotificationLevel

from odmantic import Field


class Notification:
    """Notification mixin for ODMantic models.

    Tracks per-recipient notification state: type, severity, read/seen status,
    and metadata about the triggering action.

    Note: Does not include recipient reference. Each contrib implementation
    should add recipient using ODMantic's Reference or similar.
    """

    notification_type: str = Field(
        ...,
        description=(
            "Dot-notation type identifier (e.g. 'comment.reply', 'order.shipped')"
        ),
    )
    level: NotificationLevel = Field(
        default=NotificationLevel.INFO,
        description="Severity/criticality level of notification",
    )
    title: str = Field(
        ...,
        max_length=255,
        description="Short human-readable title",
    )
    description: str | None = Field(
        default=None,
        description="Longer human-readable body",
    )
    data: dict[str, Any] | None = Field(
        default=None,
        description="Arbitrary JSON payload for extra context",
    )
    actor_type: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic type of entity that triggered notification",
    )
    actor_id: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic ID of entity that triggered notification",
    )
    action_url: str | None = Field(
        default=None,
        max_length=2048,
        description="Click-through URL for the notification",
    )
    group_key: str | None = Field(
        default=None,
        max_length=255,
        description="Grouping key for batching similar notifications",
    )
    seen_at: datetime.datetime | None = Field(
        default=None,
        description="When notification appeared in user's feed; None = unseen",
    )
    read_at: datetime.datetime | None = Field(
        default=None,
        description="When user clicked/opened notification; None = unread",
    )
    archived_at: datetime.datetime | None = Field(
        default=None,
        description="When user archived/dismissed notification; None = not archived",
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="When notification was created",
    )
