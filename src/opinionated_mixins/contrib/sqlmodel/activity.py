import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Text
from ._base import documented_field


__all__ = ["Activity"]


class Activity:
    """Activity mixin for SQLModel models.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.

    Three polymorphic pairs track the entities involved:
    - actor (required): who performed the action
    - target (optional): what the action was performed on
    - action_object (optional): what was created or used by the action

    Indexing recommendations:
    - ``actor_type``, ``actor_id``: compound index for an actor's feed.
    - ``target_type``, ``target_id``: compound index for a target's feed.
    - ``action_object_type``, ``action_object_id``: compound index for objects.
    - ``verb``: index recommended if filtering or aggregating by verb.
    - ``created_at``: index recommended for timeline ordering.
    - ``public``: include in composite indexes if filtering by visibility.
    """

    verb: str = documented_field(
        "Action performed (e.g. 'created', 'commented', 'merged')", max_length=255
    )
    description: str | None = documented_field(
        "Human-readable summary of the activity", default=None, sa_type=Text
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
        "Polymorphic type of entity that performed the action", max_length=255
    )
    actor_id: str = documented_field(
        "Polymorphic ID of entity that performed the action", max_length=255
    )
    target_type: str | None = documented_field(
        "Polymorphic type of entity the action was performed on",
        default=None,
        max_length=255,
    )
    target_id: str | None = documented_field(
        "Polymorphic ID of entity the action was performed on",
        default=None,
        max_length=255,
    )
    action_object_type: str | None = documented_field(
        "Polymorphic type of entity created/used by the action",
        default=None,
        max_length=255,
    )
    action_object_id: str | None = documented_field(
        "Polymorphic ID of entity created/used by the action",
        default=None,
        max_length=255,
    )
    public: bool = documented_field(
        "Whether activity is visible to non-participants", default=True
    )
    created_at: datetime.datetime = documented_field(
        "When activity occurred",
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
