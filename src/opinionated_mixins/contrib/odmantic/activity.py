import datetime
from typing import Any

from odmantic import Field


class Activity:
    """Activity mixin for ODMantic models.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.

    Three polymorphic pairs track the entities involved:
    - actor (required): who performed the action
    - target (optional): what the action was performed on
    - action_object (optional): what was created or used by the action
    """

    verb: str = Field(
        ...,
        max_length=255,
        description="Action performed (e.g. 'created', 'commented', 'merged')",
    )
    description: str | None = Field(
        default=None,
        description="Human-readable summary of the activity",
    )
    data: dict[str, Any] | None = Field(
        default=None,
        description="Arbitrary JSON payload for extra context",
    )
    actor_type: str = Field(
        ...,
        max_length=255,
        description="Polymorphic type of entity that performed the action",
    )
    actor_id: str = Field(
        ...,
        max_length=255,
        description="Polymorphic ID of entity that performed the action",
    )
    target_type: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic type of entity the action was performed on",
    )
    target_id: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic ID of entity the action was performed on",
    )
    action_object_type: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic type of entity created/used by the action",
    )
    action_object_id: str | None = Field(
        default=None,
        max_length=255,
        description="Polymorphic ID of entity created/used by the action",
    )
    public: bool = Field(
        default=True,
        description="Whether activity is visible to non-participants",
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="When activity occurred",
    )
