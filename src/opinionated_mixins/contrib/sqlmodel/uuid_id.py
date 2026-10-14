import uuid

from sqlmodel import Field


__all__ = ["UUIDID"]


class UUIDID:
    """UUIDID mixin for SQLModel models."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
