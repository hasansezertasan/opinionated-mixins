import datetime

from sqlalchemy import DateTime
from sqlmodel import Field


__all__ = ["CreatedAt"]


class CreatedAt:
    """CreatedAt mixin for SQLModel models.

    Native SQLModel fields: the columns are also Pydantic fields, so they can
    be passed to the constructor and assigned.

    Indexing recommendations:
    - ``created_at``: index recommended if frequently querying, sorting, or
      filtering records by creation timestamp.

    Example:
        .. code-block:: python

            class MyModel(CreatedAt, SQLModel, table=True):
                __tablename__ = "items"
                id: int | None = Field(default=None, primary_key=True)
    """

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
