from sqlalchemy import Boolean, Column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IsActive:
    """IsActive mixin for SQLAlchemy models."""

    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
