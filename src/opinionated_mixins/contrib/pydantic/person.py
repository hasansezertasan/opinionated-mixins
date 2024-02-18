import datetime

from pydantic import BaseModel, Field
from typing_extensions import Optional


class Person(BaseModel):
    """
    Pydantic `Person` model that represents a person.
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
