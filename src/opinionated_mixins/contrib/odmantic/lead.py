import datetime
from decimal import Decimal

from bson.decimal128 import Decimal128
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from pydantic import field_serializer

from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["Lead"]


class Lead(metaclass=ODManticMixinMetaclass):
    """Lead mixin for ODMantic models."""

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
    opportunity_amount: Decimal | None = Field(default=None)
    currency: str | None = Field(default=None, max_length=3)
    probability: int = Field(default=0)
    close_date: datetime.date | None = Field(default=None)
    last_contacted: datetime.date | None = Field(default=None)
    next_follow_up: datetime.date | None = Field(default=None)
    description: str | None = Field(default=None)
    is_active: bool = Field(default=True)

    @field_serializer("opportunity_amount")
    @staticmethod
    def serialize_opportunity_amount(opportunity_amount: Decimal | None) -> object:
        """Serialize decimal amounts to BSON Decimal128 values.

        Returns:
            A BSON-compatible Decimal128 value, or ``None``.
        """
        if opportunity_amount is None:
            return None
        return Decimal128(opportunity_amount)

    @field_serializer("close_date", "last_contacted", "next_follow_up")
    @staticmethod
    def serialize_date(value: datetime.date | None) -> datetime.datetime | None:
        """Serialize date-only values to BSON-compatible datetimes.

        Returns:
            A midnight datetime for BSON storage, or ``None``.
        """
        if value is None:
            return None
        return datetime.datetime.combine(value, datetime.time())
