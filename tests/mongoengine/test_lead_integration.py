"""Integration tests for MongoEngine Lead mixin."""

import datetime
from decimal import Decimal

from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus


class MyLead(Lead, Document):
    """Test model composing Lead with Document."""

    meta = {"collection": "test_leads"}


class TestLeadIntegration:
    """Test Lead mixin composition, instantiation, and roundtrip."""

    def test_create_with_defaults(self) -> None:
        obj = MyLead()
        obj.save()
        loaded = MyLead.objects.first()
        assert loaded is not None
        assert loaded.probability == 0
        assert loaded.is_active is True
        assert loaded.title is None
        assert loaded.status is None
        assert loaded.source is None
        assert loaded.rating is None

    def test_create_with_all_fields(self) -> None:
        today = datetime.date.today()
        obj = MyLead(
            title="Big Deal",
            salutation="Mr",
            job_title="CTO",
            company_name="Acme Corp",
            website="https://acme.example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
            status=LeadStatus.IN_PROCESS.value,
            source=LeadSource.EMAIL.value,
            industry="Technology",
            rating=LeadRating.HOT.value,
            opportunity_amount=Decimal("50000.00"),
            currency="USD",
            probability=75,
            close_date=today,
            last_contacted=today,
            next_follow_up=today,
            description="A big opportunity",
            is_active=True,
        )
        obj.save()
        loaded = MyLead.objects.first()
        assert loaded.title == "Big Deal"
        assert loaded.salutation == "Mr"
        assert loaded.job_title == "CTO"
        assert loaded.company_name == "Acme Corp"
        assert loaded.status == LeadStatus.IN_PROCESS.value
        assert loaded.source == LeadSource.EMAIL.value
        assert loaded.rating == LeadRating.HOT.value
        assert loaded.probability == 75
        assert loaded.currency == "USD"
        assert loaded.description == "A big opportunity"

    def test_enum_fields_roundtrip(self) -> None:
        obj = MyLead(
            status=LeadStatus.CONVERTED.value,
            source=LeadSource.PARTNER.value,
            rating=LeadRating.COLD.value,
        )
        obj.save()
        loaded = MyLead.objects.first()
        assert loaded.status == LeadStatus.CONVERTED.value
        assert loaded.source == LeadSource.PARTNER.value
        assert loaded.rating == LeadRating.COLD.value
