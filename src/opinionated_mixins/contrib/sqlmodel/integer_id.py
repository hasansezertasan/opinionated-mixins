from sqlmodel import Field


__all__ = ["IntegerID"]


class IntegerID:
    """IntegerID mixin for SQLModel models.

    ``id`` is ``None`` until the database assigns it.
    """

    id: int | None = Field(default=None, primary_key=True)
