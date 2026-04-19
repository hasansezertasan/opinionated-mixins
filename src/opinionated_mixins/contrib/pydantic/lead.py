import datetime
from decimal import Decimal

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from pydantic import Field


class Lead:
    """Lead mixin for Pydantic models."""

    title: str | None = Field(default=None, max_length=255)
    salutation: str | None = Field(default=None, max_length=64)
    job_title: str | None = Field(default=None, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=255)
    linkedin_url: str | None = Field(default=None, max_length=500)
    status: LeadStatus | None = Field(default=None)
    source: LeadSource | None = Field(default=None)
    industry: str | None = Field(default=None, max_length=255)
    rating: LeadRating | None = Field(default=None)
    opportunity_amount: Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2,
    )
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    probability: int = Field(default=0, ge=0, le=100)
    close_date: datetime.date | None = Field(default=None)
    last_contacted: datetime.date | None = Field(default=None)
    next_follow_up: datetime.date | None = Field(default=None)
    description: str | None = Field(default=None)
    is_active: bool = Field(default=True)
