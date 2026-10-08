import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField

__all__ = ["UpdatedAt"]


class UpdatedAt:
    """UpdatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    updated_at = DateTimeField(
        required=True, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
