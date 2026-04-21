import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Activity:
    """Activity mixin for SQLAlchemy models.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.

    Three polymorphic pairs track the entities involved:
    - actor (required): who performed the action
    - target (optional): what the action was performed on
    - action_object (optional): what was created or used by the action
    """

    __abstract__ = True

    verb = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Action performed (e.g. 'created', 'commented', 'merged')",
    )
    description = Column(
        Text,
        nullable=True,
        doc="Human-readable summary of the activity",
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
        doc="Polymorphic type of entity that performed the action",
    )
    actor_id = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Polymorphic ID of entity that performed the action",
    )
    target_type = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Polymorphic type of entity the action was performed on",
    )
    target_id = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Polymorphic ID of entity the action was performed on",
    )
    action_object_type = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Polymorphic type of entity created/used by the action",
    )
    action_object_id = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Polymorphic ID of entity created/used by the action",
    )
    public = Column(
        Boolean,
        nullable=False,
        index=True,
        default=True,
        doc="Whether activity is visible to non-participants",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        doc="When activity occurred",
    )
