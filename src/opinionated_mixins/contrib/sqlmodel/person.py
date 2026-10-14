import datetime

from sqlalchemy import Text
from sqlmodel import Field


__all__ = ["Person"]


class Person:
    """Person mixin for SQLModel models."""

    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    street_address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=2)
    date_of_birth: datetime.date | None = Field(default=None)
    bio: str | None = Field(default=None, sa_type=Text)
