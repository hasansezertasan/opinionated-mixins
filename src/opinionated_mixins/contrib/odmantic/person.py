import datetime
from typing import Any, cast

from odmantic import Field

from ._base import ODManticMixinMetaclass, bson_key_for_field, date_to_datetime_for_bson

__all__ = ["Person"]


class Person(metaclass=ODManticMixinMetaclass):
    """Person mixin for ODMantic models."""

    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    street_address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: datetime.date | None = Field(default=None)
    bio: str | None = Field(default=None)

    def model_dump_doc(  # pylint: disable=no-member
        self, include: object = None
    ) -> dict[str, Any]:
        """Generate a BSON document while keeping Pydantic dumps date-native.

        Returns:
            The BSON-ready document representation.
        """
        base = cast("Any", super())
        document = cast("dict[str, Any]", base.model_dump_doc(include=include))
        key_name = bson_key_for_field(type(self), "date_of_birth")
        if key_name in document:
            document[key_name] = date_to_datetime_for_bson(document[key_name])
        return document
