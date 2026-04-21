import datetime
from typing import Any, ClassVar

from mongoengine import BooleanField, DateTimeField, DictField, StringField


class Activity:
    """Activity mixin for MongoEngine documents.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.

    Three polymorphic pairs track the entities involved:
    - actor (required): who performed the action
    - target (optional): what the action was performed on
    - action_object (optional): what was created or used by the action
    """

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    verb = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text="Action performed (e.g. 'created', 'commented', 'merged')",
    )
    description = StringField(
        help_text="Human-readable summary of the activity",
    )
    data = DictField(
        default=None,
        help_text="Arbitrary JSON payload for extra context",
    )
    actor_type = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text="Polymorphic type of entity that performed the action",
    )
    actor_id = StringField(
        required=True,
        max_length=255,
        index=True,
        help_text="Polymorphic ID of entity that performed the action",
    )
    target_type = StringField(
        max_length=255,
        index=True,
        help_text="Polymorphic type of entity the action was performed on",
    )
    target_id = StringField(
        max_length=255,
        index=True,
        help_text="Polymorphic ID of entity the action was performed on",
    )
    action_object_type = StringField(
        max_length=255,
        index=True,
        help_text="Polymorphic type of entity created/used by the action",
    )
    action_object_id = StringField(
        max_length=255,
        index=True,
        help_text="Polymorphic ID of entity created/used by the action",
    )
    public = BooleanField(
        required=True,
        default=True,
        index=True,
        help_text="Whether activity is visible to non-participants",
    )
    created_at = DateTimeField(
        required=True,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        help_text="When activity occurred",
    )
