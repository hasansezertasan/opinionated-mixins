import datetime

from pydantic import Field


class User:
    """User mixin for Pydantic models."""

    username: str = Field(..., min_length=1, max_length=255)
    hashed_password: str = Field(..., min_length=1)
    email: str | None = Field(default=None, max_length=254)
    date_email_verified: datetime.datetime | None = Field(default=None)
