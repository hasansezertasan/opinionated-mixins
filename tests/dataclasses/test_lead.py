import dataclasses
import datetime
from decimal import Decimal

from opinionated_mixins.contrib.dataclasses import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

LEAD_FIELDS = {
    "title",
    "salutation",
    "job_title",
    "company_name",
    "website",
    "linkedin_url",
    "status",
    "source",
    "industry",
    "rating",
    "opportunity_amount",
    "currency",
    "probability",
    "close_date",
    "last_contacted",
    "next_follow_up",
    "description",
    "is_active",
}


class TestDataclassesLead:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(Lead)

    def test_create_defaults(self) -> None:
        obj = Lead()
        assert obj.title is None
        assert obj.status is None
        assert obj.probability == 0
        assert obj.is_active is True

    def test_create_with_all_fields(self) -> None:
        obj = Lead(
            title="Dr.",
            salutation="Dr.",
            job_title="CTO",
            company_name="Acme Inc.",
            website="https://acme.com",
            linkedin_url="https://linkedin.com/in/jane",
            status=LeadStatus.ASSIGNED,
            source=LeadSource.EMAIL,
            industry="Technology",
            rating=LeadRating.HOT,
            opportunity_amount=Decimal("50000.00"),
            currency="USD",
            probability=75,
            close_date=datetime.date(2026, 6, 1),
            last_contacted=datetime.date(2026, 4, 15),
            next_follow_up=datetime.date(2026, 4, 22),
            description="High-value lead",
            is_active=True,
        )
        assert obj.job_title == "CTO"
        assert obj.status == LeadStatus.ASSIGNED

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(Lead)}
        assert fields == LEAD_FIELDS
