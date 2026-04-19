# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.mongoengine import Person


class TestMongoEnginePerson:
    def test_has_first_name_field(self) -> None:
        assert hasattr(Person, "first_name")
        assert Person.first_name.required is True
        assert Person.first_name.max_length == 255

    def test_has_last_name_field(self) -> None:
        assert hasattr(Person, "last_name")
        assert Person.last_name.required is True
        assert Person.last_name.max_length == 255

    def test_has_middle_name_field(self) -> None:
        assert hasattr(Person, "middle_name")
        assert Person.middle_name.required is False
        assert Person.middle_name.max_length == 255

    def test_has_phone_number_field(self) -> None:
        assert hasattr(Person, "phone_number")
        assert Person.phone_number.required is False
        assert Person.phone_number.max_length == 20

    def test_has_email_field(self) -> None:
        assert hasattr(Person, "email")
        assert Person.email.required is False
        assert Person.email.max_length == 254

    def test_has_street_address_field(self) -> None:
        assert hasattr(Person, "street_address")
        assert Person.street_address.required is False
        assert Person.street_address.max_length == 255

    def test_has_postal_code_field(self) -> None:
        assert hasattr(Person, "postal_code")
        assert Person.postal_code.required is False
        assert Person.postal_code.max_length == 20

    def test_has_city_field(self) -> None:
        assert hasattr(Person, "city")
        assert Person.city.required is False
        assert Person.city.max_length == 255

    def test_has_country_field(self) -> None:
        assert hasattr(Person, "country")
        assert Person.country.required is False
        assert Person.country.max_length == 2

    def test_has_date_of_birth_field(self) -> None:
        assert hasattr(Person, "date_of_birth")
        assert Person.date_of_birth.required is False

    def test_has_bio_field(self) -> None:
        assert hasattr(Person, "bio")
        assert Person.bio.required is False
