from mongoengine import DateTimeField, StringField


class Person:
    """
    MongoEngine `Person` document that represents a person.

    !!! note
        This class does not inherit from `Document`, `EmbeddedDocument`, or any other document types and is not meant to be used directly.
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

    meta = {"allow_inheritance": True}
