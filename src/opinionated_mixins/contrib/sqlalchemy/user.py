from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin

if TYPE_CHECKING:
    import datetime

    from sqlalchemy.orm import Mapped

__all__ = ["User"]


@declarative_mixin
class User:
    """User mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``username``, ``email``: already declared with ``unique=True``, which
      creates a unique index in most relational databases; additional indexes
      on these columns are usually redundant.
    - ``date_email_verified``: index recommended if frequently filtering or
      reporting on user verification status.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyUser(User, Base):
                __tablename__ = "users"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_users_date_email_verified", "date_email_verified"),
                )
    """

    __abstract__ = True

    if TYPE_CHECKING:
        username: Mapped[str]
        hashed_password: Mapped[str]
        email: Mapped[str | None]
        date_email_verified: Mapped[datetime.datetime | None]
    else:
        username = Column(String(255), nullable=False, unique=True)
        hashed_password = Column(String(1024), nullable=False)
        email = Column(String(254), nullable=True, unique=True)
        date_email_verified = Column(DateTime, nullable=True)
