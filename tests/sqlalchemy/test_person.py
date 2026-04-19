# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import datetime

from opinionated_mixins.contrib.sqlalchemy import Person
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyPerson(Person, Base):  # type: ignore[misc]
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyPerson:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_required_only(self) -> None:
        with Session(self.engine) as session:
            obj = MyPerson(first_name="Jane", last_name="Doe")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.first_name == "Jane"
            assert obj.last_name == "Doe"
            assert obj.middle_name is None
            assert obj.phone_number is None
            assert obj.email is None
            assert obj.street_address is None
            assert obj.postal_code is None
            assert obj.city is None
            assert obj.country is None
            assert obj.date_of_birth is None
            assert obj.bio is None

    def test_create_with_all_fields(self) -> None:
        with Session(self.engine) as session:
            obj = MyPerson(
                first_name="Jane",
                last_name="Doe",
                middle_name="Marie",
                phone_number="+1234567890",
                email="jane@example.com",
                street_address="123 Main St",
                postal_code="10001",
                city="New York",
                country="US",
                date_of_birth=datetime.date(1990, 5, 15),
                bio="Software engineer",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.middle_name == "Marie"
            assert obj.phone_number == "+1234567890"
            assert obj.email == "jane@example.com"
            assert obj.street_address == "123 Main St"
            assert obj.postal_code == "10001"
            assert obj.city == "New York"
            assert obj.country == "US"
            assert obj.date_of_birth == datetime.date(1990, 5, 15)
            assert obj.bio == "Software engineer"

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyPerson.__table__.columns}
        expected = {
            "first_name",
            "last_name",
            "middle_name",
            "phone_number",
            "email",
            "street_address",
            "postal_code",
            "city",
            "country",
            "date_of_birth",
            "bio",
        }
        assert expected.issubset(columns)
