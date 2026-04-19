import datetime
from decimal import Decimal

import pytest
from opinionated_mixins.contrib.pydantic import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from pydantic import BaseModel, ValidationError


class LeadModel(Lead, BaseModel):
    pass


class TestPydanticLead:
    def test_create_defaults(self) -> None:
        obj = LeadModel()
        assert obj.title is None
        assert obj.status is None
        assert obj.probability == 0
        assert obj.is_active is True

    def test_create_with_all_fields(self) -> None:
        obj = LeadModel(
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
        assert obj.rating == LeadRating.HOT

    def test_title_max_length(self) -> None:
        with pytest.raises(ValidationError):
            LeadModel(title="x" * 256)

    def test_status_from_string(self) -> None:
        obj = LeadModel(status="ASSIGNED")
        assert obj.status == LeadStatus.ASSIGNED

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(ValidationError):
            LeadModel(status="invalid")

    def test_probability_range(self) -> None:
        with pytest.raises(ValidationError):
            LeadModel(probability=101)
        with pytest.raises(ValidationError):
            LeadModel(probability=-1)

    def test_currency_must_be_three_chars(self) -> None:
        with pytest.raises(ValidationError):
            LeadModel(currency="US")
        with pytest.raises(ValidationError):
            LeadModel(currency="USDD")
