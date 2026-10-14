"""Shared support for SQLModel mixins."""

from typing import Any

from sqlmodel import Field

__all__ = ["documented_field"]


def documented_field(doc: str, **kwargs: Any) -> Any:  # noqa: ANN401
    """Declare a ``Field`` whose text reaches both Pydantic and SQLAlchemy.

    SQLModel forwards ``description`` to Pydantic only, so the same text is also
    passed as ``Column.doc``.

    Returns:
        A ``sqlmodel.Field`` carrying ``doc`` as description and column doc.
    """
    column_kwargs = {"doc": doc, **kwargs.pop("sa_column_kwargs", {})}
    return Field(description=doc, sa_column_kwargs=column_kwargs, **kwargs)
