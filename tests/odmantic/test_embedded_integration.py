"""Integration tests for mixins composed with ODMantic embedded models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Annotated

from odmantic import EmbeddedModel, Field, Model
from odmantic.bson import WithBsonSerializer
import pytest

from opinionated_mixins.contrib.odmantic import IsActive, Lead, Person


class EmbeddedPerson(Person, EmbeddedModel):
    """A person stored within a collection model."""


class Household(Model):
    """Collection model containing a mixed-in embedded person."""

    person: EmbeddedPerson


class EmbeddedLead(Lead, EmbeddedModel):
    """A populated lead stored within another model."""


class LeadContainer(Model):
    """Collection model containing a lead."""

    lead: EmbeddedLead


async def test_embedded_mixin_roundtrip(mock_engine) -> None:
    person = EmbeddedPerson(
        first_name="Alice", last_name="Smith", date_of_birth=datetime.date(1990, 1, 15)
    )
    household = Household(person=person)

    await mock_engine.save(household)
    loaded = await mock_engine.find_one(Household)

    assert loaded is not None
    assert loaded.person == person
    assert "id" not in EmbeddedPerson.model_fields
    assert "_id" not in person.model_dump_doc()


def test_embedded_mixin_rejects_primary_field() -> None:
    with pytest.raises(TypeError, match="cannot define a primary field"):
        type(
            "InvalidEmbedded",
            (IsActive, EmbeddedModel),
            {
                "__annotations__": {"identifier": int},
                "identifier": Field(primary_field=True),
            },
        )


async def test_embedded_lead_roundtrip(mock_engine) -> None:
    lead = EmbeddedLead(
        opportunity_amount=Decimal("123.45"), close_date=datetime.date(2026, 10, 8)
    )
    await mock_engine.save(LeadContainer(lead=lead))

    loaded = await mock_engine.find_one(LeadContainer)

    assert loaded is not None
    assert loaded.lead == lead


async def test_model_first_mixins_roundtrip(mock_engine) -> None:
    class ModelFirstPerson(Model, Person):
        pass

    class ModelFirstLead(Model, Lead):
        pass

    dob = datetime.date(1990, 1, 15)
    person = ModelFirstPerson(first_name="Alice", last_name="Smith", date_of_birth=dob)
    lead = ModelFirstLead(opportunity_amount=Decimal("123.45"), close_date=dob)

    await mock_engine.save(person)
    await mock_engine.save(lead)
    loaded_person = await mock_engine.find_one(ModelFirstPerson)
    loaded_lead = await mock_engine.find_one(ModelFirstLead)

    assert loaded_person is not None
    assert loaded_lead is not None
    assert loaded_person.date_of_birth == dob
    assert loaded_lead.close_date == dob
    assert loaded_lead.opportunity_amount == Decimal("123.45")


def serialize_date(value: datetime.date) -> str:
    """Use a custom representation to verify native serializers take precedence."""
    return value.isoformat()


def test_explicit_bson_serializer_is_preserved() -> None:
    class CustomPerson(Person, EmbeddedModel):
        date_of_birth: Annotated[datetime.date, WithBsonSerializer(serialize_date)]

    person = CustomPerson(
        first_name="Alice", last_name="Smith", date_of_birth=datetime.date(1990, 1, 15)
    )

    assert person.model_dump_doc()["date_of_birth"] == "1990-01-15"
