import datetime

from opinionated_mixins.enums import NotificationLevel

from sqlalchemy import JSON, Column, DateTime, Enum, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Notification"]


@declarative_mixin
class Notification:
    """Notification mixin for SQLAlchemy models.

    Tracks per-recipient notification state: type, severity, read/seen status,
    and metadata about the triggering action.

    Note: Does not include recipient reference. Each contrib implementation
    should add recipient/recipient_id using its framework's idioms.

    Indexing recommendations:
    - ``read_at``, ``seen_at``, ``archived_at``: index (or composite index with
      recipient) recommended for querying unread, unseen, or active notifications.
    - ``created_at``: index recommended for timeline ordering.
    - ``notification_type``: index recommended if filtering notifications by type.
    - ``level``: index recommended if filtering notifications by severity.
    - ``group_key``: index recommended if batching or collapsing related notifications.
    - ``actor_type``, ``actor_id``: compound index recommended for querying by actor.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyNotification(Notification, Base):
                __tablename__ = "notifications"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_notifications_read_at", "read_at"),
                    Index("ix_notifications_created_at", "created_at"),
                    Index("ix_notifications_actor", "actor_type", "actor_id"),
                )
    """

    __abstract__ = True

    notification_type = Column(
        String(255),
        nullable=False,
        doc="Dot-notation type identifier (e.g. 'comment.reply', 'order.shipped')",
    )
    level = Column(
        Enum(NotificationLevel),
        nullable=False,
        default=NotificationLevel.INFO,
        doc="Severity/criticality level of notification",
    )
    title = Column(String(255), nullable=False, doc="Short human-readable title")
    description = Column(Text, nullable=True, doc="Longer human-readable body")
    data = Column(
        JSON,
        nullable=True,
        doc=(
            "Arbitrary JSON payload for extra context. "
            "In-place dict mutations are not tracked by SQLAlchemy; "
            "reassign the entire object to trigger change detection."
        ),
    )
    actor_type = Column(
        String(255),
        nullable=False,
        doc="Polymorphic type of entity that triggered notification",
    )
    actor_id = Column(
        String(255),
        nullable=False,
        doc="Polymorphic ID of entity that triggered notification",
    )
    action_url = Column(
        String(2048), nullable=True, doc="Click-through URL for the notification"
    )
    group_key = Column(
        String(255),
        nullable=True,
        doc="Grouping key for batching similar notifications",
    )
    seen_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When notification appeared in user's feed; None = unseen",
    )
    read_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When user clicked/opened notification; None = unread",
    )
    archived_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When user archived/dismissed notification; None = not archived",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        doc="When notification was created",
    )
