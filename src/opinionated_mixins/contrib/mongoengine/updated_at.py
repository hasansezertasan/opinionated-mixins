import datetime as dt
from typing import Any, ClassVar

from mongoengine import DateTimeField

__all__ = ["UpdatedAt"]


class UpdatedAt:
    """UpdatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    updated_at = DateTimeField(
        required=True, default=lambda: dt.datetime.now(dt.timezone.utc)
    )
