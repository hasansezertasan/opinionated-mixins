import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

__all__ = ["UpdatedAt"]


@declarative_mixin
class UpdatedAt:
    """UpdatedAt mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``updated_at``: index recommended if frequently querying, sorting, or
      filtering records by update timestamp.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyModel(UpdatedAt, Base):
                __tablename__ = "items"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_items_updated_at", "updated_at"),)
    """

    __abstract__ = True

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
