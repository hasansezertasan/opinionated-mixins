import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Text
from sqlmodel import Field


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

    verb: str = Field(max_length=255, description="Action performed (e.g. 'created')")
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
    target_type: str | None = Field(default=None, max_length=255)
    target_id: str | None = Field(default=None, max_length=255)
    action_object_type: str | None = Field(default=None, max_length=255)
    action_object_id: str | None = Field(default=None, max_length=255)
    public: bool = Field(default=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
