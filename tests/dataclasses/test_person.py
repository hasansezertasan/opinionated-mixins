# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import dataclasses
import datetime

from opinionated_mixins.contrib.dataclasses import Person


class TestDataclassesPerson:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(Person)

    def test_create_with_required_only(self) -> None:
        obj = Person(first_name="Jane", last_name="Doe")
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
        obj = Person(
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
        assert obj.country == "US"
        assert obj.date_of_birth == datetime.date(1990, 5, 15)

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(Person)}
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
        assert fields == expected
