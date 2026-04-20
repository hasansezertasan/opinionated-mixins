"""Integration tests for MongoEngine Person mixin."""

import datetime

from mongoengine import Document

from opinionated_mixins.contrib.mongoengine import Person


class MyPerson(Person, Document):
    """Test model composing Person with Document."""

    meta = {"collection": "test_persons"}


class TestPersonIntegration:
    """Test Person mixin composition, instantiation, and roundtrip."""

    def test_create_with_required_fields(self) -> None:
        obj = MyPerson(first_name="Alice", last_name="Smith")
        obj.save()
        loaded = MyPerson.objects.first()
        assert loaded is not None
        assert loaded.first_name == "Alice"
        assert loaded.last_name == "Smith"
        assert loaded.middle_name is None
        assert loaded.phone_number is None
        assert loaded.email is None

    def test_create_with_all_fields(self) -> None:
        dob = datetime.date(1990, 1, 15)
        obj = MyPerson(
            first_name="Bob",
            last_name="Jones",
            middle_name="M",
            phone_number="+1234567890",
            email="bob@example.com",
            street_address="123 Main St",
            postal_code="12345",
            city="Springfield",
            country="US",
            date_of_birth=dob,
            bio="A test person",
        )
        obj.save()
        loaded = MyPerson.objects.first()
        assert loaded.first_name == "Bob"
        assert loaded.middle_name == "M"
        assert loaded.phone_number == "+1234567890"
        assert loaded.email == "bob@example.com"
        assert loaded.street_address == "123 Main St"
        assert loaded.postal_code == "12345"
        assert loaded.city == "Springfield"
        assert loaded.country == "US"
        assert loaded.date_of_birth == dob
        assert loaded.bio == "A test person"

    def test_optional_fields_default_none(self) -> None:
        obj = MyPerson(first_name="C", last_name="D")
        obj.save()
        loaded = MyPerson.objects.first()
        assert loaded.street_address is None
        assert loaded.postal_code is None
        assert loaded.city is None
        assert loaded.country is None
        assert loaded.date_of_birth is None
        assert loaded.bio is None
