# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from sqlalchemy import Column
from sqlalchemy.orm import declarative_mixin  # type: ignore
from sqlalchemy.sql.sqltypes import Date, String


@declarative_mixin
class Person:
    """SQLAlchemy `Person` model that represents a person.

    !!! note
        This class does not inherit from any base class and is not meant to be used directly.

    !!! example
        How to override the `Person` model:
        ```python
        from opinionated_mixins.contrib.sqlalchemy.person import Person as SQLAPerson
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()


        class Person(Base, SQLAPerson):
            id = Column(Integer, primary_key=True, autoincrement=True, index=True)
            first_name = Column(String(64), nullable=True)
            last_name = Column(String(64), nullable=True)
            email = Column(String(64), index=True, unique=True)
        ```
    """

    __abstract__ = True

    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    middle_name = Column(String(64))
    phone = Column(String(64))
    email = Column(String(64))
    address = Column(String(64))
    postal_code = Column(String(64))
    city = Column(String(64))
    country = Column(String(64))
    date_birth = Column(Date)
    description = Column(String(64))
