from typing import Any, ClassVar

from mongoengine import DateTimeField, StringField


class User:
    """User mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    username = StringField(required=True, max_length=255, unique=True)
    hashed_password = StringField(required=True, max_length=1024)
    email = StringField(required=False, max_length=254, unique=True, sparse=True)
    date_email_verified = DateTimeField(required=False)
