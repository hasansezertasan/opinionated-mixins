import datetime as dt
from typing import Any, ClassVar

from mongoengine import DateTimeField

__all__ = ["CreatedAt"]


class CreatedAt:
    """CreatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}
    created_at = DateTimeField(required=True, default=lambda: dt.datetime.now(dt.UTC))
