import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Activity"]


@declarative_mixin
class Activity:
    """Activity mixin for SQLAlchemy models.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.

    Three polymorphic pairs track the entities involved:
    - actor (required): who performed the action
    - target (optional): what the action was performed on
    - action_object (optional): what was created or used by the action

    Indexing recommendations:
    - ``actor_type``, ``actor_id``: compound index recommended for querying an
      actor's activity feed.
    - ``target_type``, ``target_id``: compound index recommended for querying
      activity on a specific target.
    - ``action_object_type``, ``action_object_id``: compound index recommended
      for querying activity involving a specific object.
    - ``verb``: index recommended if filtering or aggregating by action verb.
    - ``created_at``: index recommended for timeline ordering.
    - ``public``: include in composite indexes if filtering feeds by visibility.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyActivity(Activity, Base):
                __tablename__ = "activities"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_activities_actor", "actor_type", "actor_id"),
                    Index("ix_activities_target", "target_type", "target_id"),
                    Index("ix_activities_created_at", "created_at"),
                )
    """

    __abstract__ = True

    verb = Column(
        String(255),
        nullable=False,
        doc="Action performed (e.g. 'created', 'commented', 'merged')",
    )
    description = Column(
        Text, nullable=True, doc="Human-readable summary of the activity"
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
        doc="Polymorphic type of entity that performed the action",
    )
    actor_id = Column(
        String(255),
        nullable=False,
        doc="Polymorphic ID of entity that performed the action",
    )
    target_type = Column(
        String(255),
        nullable=True,
        doc="Polymorphic type of entity the action was performed on",
    )
    target_id = Column(
        String(255),
        nullable=True,
        doc="Polymorphic ID of entity the action was performed on",
    )
    action_object_type = Column(
        String(255),
        nullable=True,
        doc="Polymorphic type of entity created/used by the action",
    )
    action_object_id = Column(
        String(255),
        nullable=True,
        doc="Polymorphic ID of entity created/used by the action",
    )
    public = Column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether activity is visible to non-participants",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        doc="When activity occurred",
    )
