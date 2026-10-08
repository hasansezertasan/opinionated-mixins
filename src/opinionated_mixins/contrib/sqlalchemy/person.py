from sqlalchemy import Column, Date, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Person"]


@declarative_mixin
class Person:
    """Person mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``last_name``, ``first_name``: compound index recommended for name lookups
      and sorting.
    - ``email``: index recommended if looking up people by email address.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyPerson(Person, Base):
                __tablename__ = "people"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_people_name", "last_name", "first_name"),
                    Index("ix_people_email", "email"),
                )
    """

    __abstract__ = True

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(254), nullable=True)
    street_address = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(2), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)
