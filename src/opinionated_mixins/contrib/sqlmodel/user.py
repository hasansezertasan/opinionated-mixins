import datetime as dt

from sqlalchemy import DateTime
from sqlmodel import Field


__all__ = ["User"]


class User:
    """User mixin for SQLModel models.

    Indexing recommendations:
    - ``username``, ``email``: already declared with ``unique=True``, which
      creates a unique index in most relational databases; additional indexes
      on these columns are usually redundant.
    - ``date_email_verified``: index recommended if frequently filtering or
      reporting on user verification status.
    """

    username: str = Field(max_length=255, unique=True)
    hashed_password: str = Field(max_length=1024)
    email: str | None = Field(default=None, max_length=254, unique=True)
    date_email_verified: dt.datetime | None = Field(default=None, sa_type=DateTime)
