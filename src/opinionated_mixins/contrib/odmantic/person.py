import datetime

from pydantic import field_serializer

from odmantic import Field

from ._base import ODManticMixinMetaclass

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

    @field_serializer("date_of_birth")
    @staticmethod
    def serialize_date_of_birth(
        date_of_birth: datetime.date | None,
    ) -> datetime.datetime | None:
        """Serialize date-only values to BSON-compatible datetimes.

        Returns:
            A midnight datetime for BSON storage, or ``None``.
        """
        if date_of_birth is None:
            return None
        return datetime.datetime.combine(date_of_birth, datetime.time())
