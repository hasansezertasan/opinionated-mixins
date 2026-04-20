"""Integration tests for ODMantic Person mixin."""

import datetime

import pytest
from odmantic import Model

from opinionated_mixins.contrib.odmantic import Person


pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/TODO",
    strict=True,
)


class MyPerson(Person, Model):
    """Test model composing Person with Model."""

    model_config = {"collection": "test_persons"}


class TestPersonIntegration:
    """Test Person mixin composition, instantiation, and roundtrip."""

    async def test_create_with_required_fields(self, mock_engine) -> None:
        obj = MyPerson(first_name="Alice", last_name="Smith")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyPerson)
        assert loaded is not None
        assert loaded.first_name == "Alice"
        assert loaded.last_name == "Smith"
        assert loaded.middle_name is None
        assert loaded.phone_number is None
        assert loaded.email is None

    async def test_create_with_all_fields(self, mock_engine) -> None:
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
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyPerson)
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

    async def test_optional_fields_default_none(self, mock_engine) -> None:
        obj = MyPerson(first_name="C", last_name="D")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyPerson)
        assert loaded.street_address is None
        assert loaded.postal_code is None
        assert loaded.city is None
        assert loaded.country is None
        assert loaded.date_of_birth is None
        assert loaded.bio is None
