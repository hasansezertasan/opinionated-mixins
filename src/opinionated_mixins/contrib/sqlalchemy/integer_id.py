from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

__all__ = ["IntegerID"]


@declarative_mixin
class IntegerID:
    """IntegerID mixin for SQLAlchemy models."""

    __abstract__ = True

    if TYPE_CHECKING:
        id: Mapped[int]
    else:
        id = Column(Integer, primary_key=True, autoincrement=True)
