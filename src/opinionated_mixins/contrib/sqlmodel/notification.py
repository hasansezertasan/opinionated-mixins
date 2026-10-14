import datetime
from typing import Any

from opinionated_mixins.enums import NotificationLevel
from sqlalchemy import JSON, DateTime, Text
from sqlmodel import Field


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

    notification_type: str = Field(
        max_length=255,
        description="Dot-notation type identifier (e.g. 'order.shipped')",
    )
    level: NotificationLevel = Field(default=NotificationLevel.INFO)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, sa_type=Text)
    data: dict[str, Any] | None = Field(
        default=None,
        sa_type=JSON,
        description=(
            "Arbitrary JSON payload. In-place dict mutations are not tracked; "
            "reassign the entire object to trigger change detection."
        ),
    )
    actor_type: str = Field(max_length=255)
    actor_id: str = Field(max_length=255)
    action_url: str | None = Field(default=None, max_length=2048)
    group_key: str | None = Field(default=None, max_length=255)
    seen_at: datetime.datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )
    read_at: datetime.datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )
    archived_at: datetime.datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
