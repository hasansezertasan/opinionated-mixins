# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT

from sqlalchemy import Column, Date, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Person:
    """Person mixin for SQLAlchemy models."""

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
