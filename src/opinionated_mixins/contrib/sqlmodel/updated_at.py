import datetime as dt

from sqlalchemy import DateTime
from sqlmodel import Field


__all__ = ["UpdatedAt"]


class UpdatedAt:
    """UpdatedAt mixin for SQLModel models.

    Indexing recommendations:
    - ``updated_at``: index recommended if frequently querying, sorting, or
      filtering records by update timestamp.
    """

    updated_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": lambda: dt.datetime.now(dt.timezone.utc)},
    )
