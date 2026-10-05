import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField


class CreatedAt:
    """CreatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}
    created_at = DateTimeField(
        required=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
