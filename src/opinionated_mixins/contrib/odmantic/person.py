# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import datetime
from typing import Optional

from odmantic import Field


class Person:
    """ODMantic `Person` model that represents a person.

    !!! note
        This class does not inherit from `Model`, `EmbeddedModel`, or any other document types and is not meant to be used directly.

    !!! example
        How to override the `Person` model:
        ```python
        from odmantic import Field, Model
        from opinionated_mixins.contrib.odmantic.person import Person as ODMPerson
        from typing_extensions import Optional


        class Person(Model, ODMPerson):
            first_name: Optional[str] = Field(min_length=1, max_length=64)
            last_name: Optional[str] = Field(min_length=1, max_length=64)
        ```
    """

    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    phone: Optional[str] = Field(default=None, min_length=1, max_length=64)
    email: Optional[str] = Field(default=None, min_length=1, max_length=64)
    address: Optional[str] = Field(default=None, min_length=1, max_length=64)
    postal_code: Optional[str] = Field(default=None, min_length=1, max_length=64)
    city: Optional[str] = Field(default=None, min_length=1, max_length=64)
    country: Optional[str] = Field(default=None, min_length=1, max_length=64)
    date_birth: Optional[datetime.date] = Field(default=None)
    description: Optional[str] = Field(default=None, min_length=1, max_length=64)
