from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin

__all__ = ["User"]


@declarative_mixin
class User:
    """User mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``username``, ``email``: already declared with ``unique=True``, which
      creates a unique index in most relational databases. If additional indexes
      (e.g., case-insensitive or functional) are needed, declare them explicitly
      via ``__table_args__``.

    Example:
        .. code-block:: python

            from sqlalchemy import Index, func


            class MyUser(User, Base):
                __tablename__ = "users"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_users_lower_email", func.lower(User.email)),
                )
    """

    __abstract__ = True

    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False)
    email = Column(String(254), nullable=True, unique=True)
    date_email_verified = Column(DateTime, nullable=True)
