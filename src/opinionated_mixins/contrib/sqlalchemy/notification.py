import datetime

from opinionated_mixins.enums import NotificationLevel

from sqlalchemy import JSON, Column, DateTime, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Notification:
    """Notification mixin for SQLAlchemy models.

    Tracks per-recipient notification state: type, severity, read/seen status,
    and metadata about the triggering action.

    Note: Does not include recipient reference. Each contrib implementation
    should add recipient/recipient_id using its framework's idioms.
    """

    __abstract__ = True

    notification_type = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Dot-notation type identifier (e.g. 'comment.reply', 'order.shipped')",
    )
    level = Column(
        Enum(NotificationLevel),
        nullable=False,
        index=True,
        default=NotificationLevel.INFO,
        doc="Severity/criticality level of notification",
    )
    title = Column(
        String(255),
        nullable=False,
        doc="Short human-readable title",
    )
    description = Column(
        Text,
        nullable=True,
        doc="Longer human-readable body",
    )
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
        index=True,
        doc="Polymorphic type of entity that triggered notification",
    )
    actor_id = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Polymorphic ID of entity that triggered notification",
    )
    action_url = Column(
        String(2048),
        nullable=True,
        doc="Click-through URL for the notification",
    )
    group_key = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Grouping key for batching similar notifications",
    )
    seen_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="When notification appeared in user's feed; None = unseen",
    )
    read_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="When user clicked/opened notification; None = unread",
    )
    archived_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="When user archived/dismissed notification; None = not archived",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        doc="When notification was created",
    )
