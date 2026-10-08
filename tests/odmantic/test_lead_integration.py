"""Integration tests for ODMantic Lead mixin."""

import datetime
from decimal import Decimal

from bson.decimal128 import Decimal128
from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus


class MyLead(Lead, Model):
    """Test model composing Lead with Model."""

    model_config = {"collection": "test_leads"}


class RenamedLead(Lead, Model):
    """Test model overriding Lead BSON field keys."""

    model_config = {"collection": "test_renamed_leads"}
    opportunity_amount: Decimal | None = Field(default=None, key_name="amount")
    close_date: datetime.date | None = Field(default=None, key_name="closed_on")
    last_contacted: datetime.date | None = Field(default=None, key_name="contacted_on")
    next_follow_up: datetime.date | None = Field(
        default=None, key_name="followed_up_on"
    )


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
        assert loaded.opportunity_amount == Decimal("50000.00")
        assert loaded.probability == 75
        assert loaded.close_date == today
        assert loaded.last_contacted == today
        assert loaded.next_follow_up == today
        assert loaded.currency == "USD"
        assert loaded.description == "A big opportunity"

    def test_bson_document_serializes_dates_without_changing_pydantic_dump(
        self,
    ) -> None:
        """Date and decimal values use BSON-safe values only in document dumps."""
        today = datetime.date.today()
        obj = MyLead(
            opportunity_amount=Decimal("50000.00"),
            close_date=today,
            last_contacted=today,
            next_follow_up=today,
        )

        pydantic_dump = obj.model_dump()
        document_dump = obj.model_dump_doc()

        assert pydantic_dump["opportunity_amount"] == Decimal("50000.00")
        assert pydantic_dump["close_date"] == today
        assert pydantic_dump["last_contacted"] == today
        assert pydantic_dump["next_follow_up"] == today
        assert document_dump["opportunity_amount"] == Decimal128("50000.00")
        assert document_dump["close_date"] == datetime.datetime.combine(
            today, datetime.time()
        )
        assert document_dump["last_contacted"] == datetime.datetime.combine(
            today, datetime.time()
        )
        assert document_dump["next_follow_up"] == datetime.datetime.combine(
            today, datetime.time()
        )

    def test_bson_document_serializes_renamed_fields(self) -> None:
        """BSON conversion honors concrete ODMantic key_name overrides."""
        today = datetime.date.today()
        obj = RenamedLead(
            opportunity_amount=Decimal("50000.00"),
            close_date=today,
            last_contacted=today,
            next_follow_up=today,
        )

        document_dump = obj.model_dump_doc()

        assert document_dump["amount"] == Decimal128("50000.00")
        assert document_dump["closed_on"] == datetime.datetime.combine(
            today, datetime.time()
        )
        assert document_dump["contacted_on"] == datetime.datetime.combine(
            today, datetime.time()
        )
        assert document_dump["followed_up_on"] == datetime.datetime.combine(
            today, datetime.time()
        )

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
