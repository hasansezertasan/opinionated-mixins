from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class User:
    """User mixin for SQLAlchemy models."""

    __abstract__ = True

    username = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(1024), nullable=False)
    email = Column(String(254), nullable=True, unique=True, index=True)
    date_email_verified = Column(DateTime, nullable=True)
