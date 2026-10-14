import datetime
import decimal

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from sqlalchemy import Text
from sqlmodel import Field


__all__ = ["Lead"]


class Lead:
    """Lead mixin for SQLModel models.

    Indexing recommendations:
    - ``status``: index recommended if filtering leads by pipeline stage.
    - ``rating``: index recommended if querying high-priority leads.
    - ``company_name``: index recommended if searching leads by company.
    """

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
    opportunity_amount: decimal.Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2
    )
    currency: str | None = Field(default=None, max_length=3)
    probability: int | None = Field(default=0)
    close_date: datetime.date | None = Field(default=None)
    last_contacted: datetime.date | None = Field(default=None)
    next_follow_up: datetime.date | None = Field(default=None)
    description: str | None = Field(default=None, sa_type=Text)
    is_active: bool = Field(default=True)
