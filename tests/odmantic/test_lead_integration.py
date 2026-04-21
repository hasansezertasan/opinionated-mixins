"""Integration tests for ODMantic Lead mixin."""

import datetime
from decimal import Decimal

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyLead(Lead, Model):
    """Test model composing Lead with Model."""

    model_config = {"collection": "test_leads"}


class TestLeadIntegration:
    """Test Lead mixin composition, instantiation, and roundtrip."""

    async def test_create_with_defaults(self, mock_engine) -> None:
        obj = MyLead()
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyLead)
        assert loaded is not None
        assert loaded.probability == 0
        assert loaded.is_active is True
        assert loaded.title is None
        assert loaded.status is None
        assert loaded.source is None
        assert loaded.rating is None

    async def test_create_with_all_fields(self, mock_engine) -> None:
        today = datetime.date.today()
        obj = MyLead(
            title="Big Deal",
            salutation="Mr",
            job_title="CTO",
            company_name="Acme Corp",
            website="https://acme.example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
            status=LeadStatus.IN_PROCESS,
            source=LeadSource.EMAIL,
            industry="Technology",
            rating=LeadRating.HOT,
            opportunity_amount=Decimal("50000.00"),
            currency="USD",
            probability=75,
            close_date=today,
            last_contacted=today,
            next_follow_up=today,
            description="A big opportunity",
            is_active=True,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyLead)
        assert loaded.title == "Big Deal"
        assert loaded.salutation == "Mr"
        assert loaded.job_title == "CTO"
        assert loaded.company_name == "Acme Corp"
        assert loaded.status == LeadStatus.IN_PROCESS
        assert loaded.source == LeadSource.EMAIL
        assert loaded.rating == LeadRating.HOT
        assert loaded.probability == 75
        assert loaded.currency == "USD"
        assert loaded.description == "A big opportunity"

    async def test_enum_fields_roundtrip(self, mock_engine) -> None:
        obj = MyLead(
            status=LeadStatus.CONVERTED,
            source=LeadSource.PARTNER,
            rating=LeadRating.COLD,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyLead)
        assert loaded.status == LeadStatus.CONVERTED
        assert loaded.source == LeadSource.PARTNER
        assert loaded.rating == LeadRating.COLD
