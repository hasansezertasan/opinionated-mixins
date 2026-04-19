from typing import Any, ClassVar

from mongoengine import BooleanField


class IsActive:
    """IsActive mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    is_active = BooleanField(required=True, default=True)
