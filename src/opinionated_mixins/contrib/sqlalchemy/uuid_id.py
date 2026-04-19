import uuid

from sqlalchemy import Column, Uuid
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UUIDID:
    """UUIDID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
