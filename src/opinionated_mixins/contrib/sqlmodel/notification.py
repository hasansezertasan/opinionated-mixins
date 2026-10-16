import datetime as dt
from typing import Any

from opinionated_mixins.contrib.sqlmodel._base import documented_field
from opinionated_mixins.enums import NotificationLevel
from sqlalchemy import JSON, DateTime, Text


__all__ = ["Notification"]


class Notification:
    """Notification mixin for SQLModel models.

    Per-recipient notification tracking.

    Indexing recommendations:
    - ``notification_type``: index recommended if filtering by type.
    - ``group_key``: index recommended if batching similar notifications.
    - ``seen_at``, ``read_at``, ``archived_at``: composite index recommended
      for unread/unseen queries.
    - ``created_at``: index recommended for feed ordering.
    """

    notification_type: str = documented_field(
        "Dot-notation type identifier (e.g. 'comment.reply', 'order.shipped')",
        max_length=255,
    )
    level: NotificationLevel = documented_field(
        "Severity/criticality level of notification", default=NotificationLevel.INFO
    )
    title: str = documented_field("Short human-readable title", max_length=255)
    description: str | None = documented_field(
        "Longer human-readable body", default=None, sa_type=Text
    )
    data: dict[str, Any] | None = documented_field(
        (
            "Arbitrary JSON payload for extra context. "
            "In-place dict mutations are not tracked by SQLAlchemy; "
            "reassign the entire object to trigger change detection."
        ),
        default=None,
        sa_type=JSON,
    )
    actor_type: str = documented_field(
        "Polymorphic type of entity that triggered notification", max_length=255
    )
    actor_id: str = documented_field(
        "Polymorphic ID of entity that triggered notification", max_length=255
    )
    action_url: str | None = documented_field(
        "Click-through URL for the notification", default=None, max_length=2048
    )
    group_key: str | None = documented_field(
        "Grouping key for batching similar notifications", default=None, max_length=255
    )
    seen_at: dt.datetime | None = documented_field(
        "When notification appeared in user's feed; None = unseen",
        default=None,
        sa_type=DateTime(timezone=True),
    )
    read_at: dt.datetime | None = documented_field(
        "When user clicked/opened notification; None = unread",
        default=None,
        sa_type=DateTime(timezone=True),
    )
    archived_at: dt.datetime | None = documented_field(
        "When user archived/dismissed notification; None = not archived",
        default=None,
        sa_type=DateTime(timezone=True),
    )
    created_at: dt.datetime = documented_field(
        "When notification was created",
        default_factory=lambda: dt.datetime.now(dt.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
