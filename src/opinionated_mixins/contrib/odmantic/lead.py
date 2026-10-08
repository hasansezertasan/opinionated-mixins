import datetime
from decimal import Decimal
from typing import Any, cast

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from odmantic import Field

from ._base import (
    ODManticMixinMetaclass,
    date_to_datetime_for_bson,
    decimal_to_decimal128_for_bson,
)

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

    def model_dump_doc(  # pylint: disable=no-member
        self, include: object = None
    ) -> dict[str, Any]:
        """Generate a BSON document while keeping Pydantic dumps date-native.

        Returns:
            The BSON-ready document representation.
        """
        base = cast("Any", super())
        document = cast("dict[str, Any]", base.model_dump_doc(include=include))
        for field_name in ("close_date", "last_contacted", "next_follow_up"):
            if field_name in document:
                document[field_name] = date_to_datetime_for_bson(document[field_name])
        if "opportunity_amount" in document:
            document["opportunity_amount"] = decimal_to_decimal128_for_bson(
                document["opportunity_amount"]
            )
        return document
