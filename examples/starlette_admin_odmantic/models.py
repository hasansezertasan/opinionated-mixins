# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import datetime
from typing import Optional

from opinionated_mixins.contrib.odmantic.person import Person as ODMPerson  # noqa: ERA001
from odmantic import Field, Model


class Person(Model):
    first_name: Optional[str] = Field(min_length=1, max_length=64)
    last_name: Optional[str] = Field(min_length=1, max_length=64)
    # Inherits from ODMPerson
    # first_name: str = Field(..., min_length=1, max_length=64)  # noqa: ERA001
    # last_name: str = Field(..., min_length=1, max_length=64)  # noqa: ERA001
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    phone: Optional[str] = Field(default=None, min_length=1, max_length=64)
    email: Optional[str] = Field(default=None, min_length=1, max_length=64)
    address: Optional[str] = Field(default=None, min_length=1, max_length=64)
    postal_code: Optional[str] = Field(default=None, min_length=1, max_length=64)
    city: Optional[str] = Field(default=None, min_length=1, max_length=64)
    country: Optional[str] = Field(default=None, min_length=1, max_length=64)
    date_birth: Optional[datetime.date] = Field(default=None)
    description: Optional[str] = Field(default=None, min_length=1, max_length=64)
