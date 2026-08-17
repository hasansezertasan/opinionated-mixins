# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from typing import Any, ClassVar, Dict

from mongoengine import DateTimeField, StringField


class Person:
    """MongoEngine `Person` document that represents a person.

    !!! note
        This class does not inherit from `Document`, `EmbeddedDocument`, or any other document types and is not meant to be used directly.

    !!! example
        How to override the `Person` model:
        ```python
        from mongoengine import Document, StringField
        from opinionated_mixins.contrib.mongoengine.person import Person as MEPerson


        class Person(Document, MEPerson):
            first_name = StringField(required=False, min_length=1, max_length=64)
            last_name = StringField(required=False, min_length=1, max_length=64)
        ```
    """

    first_name = StringField(required=True, min_length=1, max_length=64)
    last_name = StringField(required=True, min_length=1, max_length=64)
    middle_name = StringField(min_length=1, max_length=64)
    phone = StringField(min_length=1, max_length=64)
    email = StringField(min_length=1, max_length=64)
    address = StringField(min_length=1, max_length=64)
    postal_code = StringField(min_length=1, max_length=64)
    city = StringField(min_length=1, max_length=64)
    country = StringField(min_length=1, max_length=64)
    date_birth = DateTimeField()
    description = StringField(min_length=1, max_length=64)

    meta: ClassVar[Dict[str, Any]] = {"allow_inheritance": True}
