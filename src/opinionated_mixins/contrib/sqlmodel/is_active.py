from sqlmodel import Field


__all__ = ["IsActive"]


class IsActive:
    """IsActive mixin for SQLModel models.

    Indexing recommendations:
    - ``is_active``: index (or composite index with other filtered columns)
      recommended if queries frequently filter active vs inactive records.
    """

    is_active: bool = Field(default=True)
