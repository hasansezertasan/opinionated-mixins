import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, Uuid
from sqlalchemy.orm import declarative_mixin

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

__all__ = ["UUIDID"]


@declarative_mixin
class UUIDID:
    """UUIDID mixin for SQLAlchemy models."""

    __abstract__ = True

    if TYPE_CHECKING:
        id: Mapped[uuid.UUID]
    else:
        id = Column(Uuid, primary_key=True, default=uuid.uuid4)
