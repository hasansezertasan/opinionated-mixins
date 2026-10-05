from __future__ import annotations

import datetime  # noqa: TC003 - ODMantic resolves annotations at runtime.

from odmantic import Field, Model


class Person(Model):
    # ODMantic does not collect fields from plain mixin parents (issue #39).
    # Declare the Person fields directly; BSON dates use datetime here.
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    street_address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: datetime.datetime | None = Field(default=None)
    bio: str | None = Field(default=None)
