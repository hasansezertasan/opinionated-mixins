from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IntegerID:
    """IntegerID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
