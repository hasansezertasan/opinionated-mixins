import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

__all__ = ["CreatedAt"]


@declarative_mixin
class CreatedAt:
    """CreatedAt mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``created_at``: index recommended if frequently querying, sorting, or
      filtering records by creation timestamp.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyModel(CreatedAt, Base):
                __tablename__ = "items"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_items_created_at", "created_at"),)
    """

    __abstract__ = True
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
