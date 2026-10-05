from typing import Any, ClassVar

from mongoengine import DateField, StringField


class Person:
    """Person mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    first_name = StringField(required=True, max_length=255)
    last_name = StringField(required=True, max_length=255)
    middle_name = StringField(required=False, max_length=255)
    phone_number = StringField(required=False, max_length=20)
    email = StringField(required=False, max_length=254)
    street_address = StringField(required=False, max_length=255)
    postal_code = StringField(required=False, max_length=20)
    city = StringField(required=False, max_length=255)
    country = StringField(required=False, max_length=2)
    date_of_birth = DateField(required=False)
    bio = StringField(required=False)
