# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class Person(BaseModel):
    """Pydantic `Person` model that represents a person."""

    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    phone: Optional[str] = Field(default=None, min_length=1, max_length=64)
    email: Optional[EmailStr] = Field(default=None)
    address: Optional[str] = Field(default=None, min_length=1, max_length=64)
    postal_code: Optional[str] = Field(default=None, min_length=1, max_length=64)
    city: Optional[str] = Field(default=None, min_length=1, max_length=64)
    country: Optional[str] = Field(default=None, min_length=1, max_length=64)
    date_birth: Optional[datetime.date] = Field(default=None)
    description: Optional[str] = Field(default=None, min_length=1, max_length=64)
