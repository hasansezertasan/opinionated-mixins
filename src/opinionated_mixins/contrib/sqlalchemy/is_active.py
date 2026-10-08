from sqlalchemy import Boolean, Column
from sqlalchemy.orm import declarative_mixin

__all__ = ["IsActive"]


@declarative_mixin
class IsActive:
    """IsActive mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``is_active``: index (or composite index with other filtered columns)
      recommended if queries frequently filter active vs inactive records.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyModel(IsActive, Base):
                __tablename__ = "items"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_items_is_active", "is_active"),)
    """

    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
