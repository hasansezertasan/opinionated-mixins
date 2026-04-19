# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.wtforms import Person
from wtforms import Form


class PersonForm(Person, Form):  # type: ignore[misc]
    pass


PERSON_FIELDS = {
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


class TestWTFormsPerson:
    def test_has_fields(self) -> None:
        form = PersonForm()
        for field_name in PERSON_FIELDS:
            assert field_name in form._fields, f"Missing field: {field_name}"

    def test_valid_submission_required_only(self) -> None:
        form = PersonForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
            },
        )
        assert form.validate()

    def test_valid_submission_all_fields(self) -> None:
        form = PersonForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "middle_name": "Marie",
                "phone_number": "+1234567890",
                "email": "jane@example.com",
                "street_address": "123 Main St",
                "postal_code": "10001",
                "city": "New York",
                "country": "US",
                "date_of_birth": "1990-05-15",
                "bio": "Software engineer",
            },
        )
        assert form.validate()

    def test_missing_first_name_invalid(self) -> None:
        form = PersonForm(
            data={
                "last_name": "Doe",
            },
        )
        assert not form.validate()
        assert "first_name" in form.errors

    def test_missing_last_name_invalid(self) -> None:
        form = PersonForm(
            data={
                "first_name": "Jane",
            },
        )
        assert not form.validate()
        assert "last_name" in form.errors
