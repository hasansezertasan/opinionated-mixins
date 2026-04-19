# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import datetime

import pytest
from opinionated_mixins.contrib.pydantic import Person
from pydantic import ValidationError


class TestPydanticPerson:
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
        assert obj.middle_name == "Marie"
        assert obj.country == "US"
        assert obj.date_of_birth == datetime.date(1990, 5, 15)

    def test_first_name_required(self) -> None:
        with pytest.raises(ValidationError):
            Person(last_name="Doe")  # type: ignore[call-arg]

    def test_last_name_required(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="Jane")  # type: ignore[call-arg]

    def test_empty_first_name_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="", last_name="Doe")

    def test_first_name_max_length(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="x" * 256, last_name="Doe")

    def test_country_must_be_two_chars(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="Jane", last_name="Doe", country="USA")

    def test_country_too_short(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="Jane", last_name="Doe", country="U")

    def test_phone_number_max_length(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="Jane", last_name="Doe", phone_number="x" * 21)

    def test_email_max_length(self) -> None:
        with pytest.raises(ValidationError):
            Person(first_name="Jane", last_name="Doe", email="x" * 255)
