---
rfc: "0012"
title: Lead
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 28
supersedes: null
superseded_by: null
---

# RFC-0012: Lead

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #28 before this process existed.

## Summary

A `Lead` mixin modelling a CRM sales lead / opportunity: contact and company
details, pipeline `status`/`source`/`rating` enums, opportunity value and
probability, and follow-up dates.

## Motivation

CRM-style lead tracking is a large, well-established domain. Rather than invent
field names, this mixin mirrors the vocabulary of the dominant CRM (Salesforce)
so the shape is instantly familiar and interoperable.

## Research

### Field Naming

| Source | Fields mirrored | Link |
| ------ | --------------- | ---- |
| Salesforce Lead | `Salutation`, `Title`(job title), `Company`, `Website`, `Industry`, `LeadSource`, `Status`, `Rating` | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_lead.htm |
| Salesforce Opportunity | `Amount`, `Probability`, `CloseDate` | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_opportunity.htm |
| HubSpot / Zoho CRM | lead source, status, rating, follow-up dates | https://developers.hubspot.com/docs/api/crm/contacts |

**Chosen names.** Field names map directly onto Salesforce's Lead and
Opportunity objects (`salutation`, `job_title`, `company_name`, `website`,
`industry`, `status`, `source`, `rating`, `opportunity_amount`, `probability`,
`close_date`), plus practical follow-up fields (`last_contacted`,
`next_follow_up`) and a `currency` for the amount. Most fields are optional
because leads are captured incrementally.

### Enum Values

| Enum | Values | Basis |
| ---- | ------ | ----- |
| `LeadStatus` | ASSIGNED, IN_PROCESS, CONVERTED, RECYCLED, CLOSED | Salesforce lead statuses |
| `LeadSource` | CALL, EMAIL, EXISTING_CUSTOMER, PARTNER, PUBLIC_RELATIONS, CAMPAIGN, OTHER | Salesforce `LeadSource` picklist |
| `LeadRating` | HOT, WARM, COLD | Salesforce `Rating` picklist |

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `title` | `str \| None` | no | `None` | `String(255)` |
| `salutation` | `str \| None` | no | `None` | `String(64)` |
| `job_title` | `str \| None` | no | `None` | `String(255)` |
| `company_name` | `str \| None` | no | `None` | `String(255)` |
| `website` | `str \| None` | no | `None` | `String(255)` |
| `linkedin_url` | `str \| None` | no | `None` | `String(500)` |
| `status` | `LeadStatus \| None` | no | `None` | enum |
| `source` | `LeadSource \| None` | no | `None` | enum |
| `industry` | `str \| None` | no | `None` | `String(255)` |
| `rating` | `LeadRating \| None` | no | `None` | enum |
| `opportunity_amount` | `Decimal \| None` | no | `None` | `Numeric(12, 2)` (SA) |
| `currency` | `str \| None` | no | `None` | `String(3)` (ISO 4217) |
| `probability` | `int` | no | `0` | percentage |
| `close_date` | `date \| None` | no | `None` | `Date` |
| `last_contacted` | `date \| None` | no | `None` | `Date` |
| `next_follow_up` | `date \| None` | no | `None` | `Date` |
| `description` | `str \| None` | no | `None` | `Text` |
| `is_active` | `bool` | no | `True` | — |

### Enum Additions

```python
# src/opinionated_mixins/enums.py
class LeadStatus(_AutoStrEnum):
    ASSIGNED = enum.auto()
    IN_PROCESS = enum.auto()
    CONVERTED = enum.auto()
    RECYCLED = enum.auto()
    CLOSED = enum.auto()


class LeadSource(_AutoStrEnum):
    CALL = enum.auto()
    EMAIL = enum.auto()
    EXISTING_CUSTOMER = enum.auto()
    PARTNER = enum.auto()
    PUBLIC_RELATIONS = enum.auto()
    CAMPAIGN = enum.auto()
    OTHER = enum.auto()


class LeadRating(_AutoStrEnum):
    HOT = enum.auto()
    WARM = enum.auto()
    COLD = enum.auto()
```

### Reference Implementation

```python
# SQLAlchemy
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from sqlalchemy import Boolean, Column, Date, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Lead:
    """Lead mixin for SQLAlchemy models."""

    __abstract__ = True

    title = Column(String(255), nullable=True)
    salutation = Column(String(64), nullable=True)
    job_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    status = Column(Enum(LeadStatus), nullable=True)
    source = Column(Enum(LeadSource), nullable=True)
    industry = Column(String(255), nullable=True)
    rating = Column(Enum(LeadRating), nullable=True)
    opportunity_amount = Column(Numeric(precision=12, scale=2), nullable=True)
    currency = Column(String(3), nullable=True)
    probability = Column(Integer, nullable=True, default=0)
    close_date = Column(Date, nullable=True)
    last_contacted = Column(Date, nullable=True)
    next_follow_up = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
```

```python
# MongoEngine
from typing import Any, ClassVar

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from mongoengine import BooleanField, DateField, DecimalField, IntField, StringField


class Lead:
    """Lead mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    title = StringField(required=False, max_length=255)
    salutation = StringField(required=False, max_length=64)
    job_title = StringField(required=False, max_length=255)
    company_name = StringField(required=False, max_length=255)
    website = StringField(required=False, max_length=255)
    linkedin_url = StringField(required=False, max_length=500)
    status = StringField(required=False, choices=[s.value for s in LeadStatus])
    source = StringField(required=False, choices=[s.value for s in LeadSource])
    industry = StringField(required=False, max_length=255)
    rating = StringField(required=False, choices=[r.value for r in LeadRating])
    opportunity_amount = DecimalField(required=False, precision=2)
    currency = StringField(required=False, max_length=3)
    probability = IntField(required=False, default=0)
    close_date = DateField(required=False)
    last_contacted = DateField(required=False)
    next_follow_up = DateField(required=False)
    description = StringField(required=False)
    is_active = BooleanField(required=False, default=True)
```

```python
# ODMantic
import datetime
from decimal import Decimal

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from odmantic import Field


class Lead:
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
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **Splitting Lead and Opportunity into two mixins** — rejected: Salesforce
   separates them, but for a mixin the combined lead-with-opportunity fields are
   more convenient; consumers can ignore the opportunity fields.
2. **Free-form string status/source/rating** — rejected: enums mirror the
   Salesforce picklists and keep pipeline reporting consistent.
3. **Storing amount as float** — rejected: `Numeric(12, 2)` / `Decimal` avoids
   floating-point money errors.

## Discussion Summary

Backfilled — original discussion on PR #28. Field and enum names were taken from
the Salesforce Lead and Opportunity objects.

## Consequences

- Implemented across all four contrib modules with identical field names.
- Adds three enums to `enums.py`.
- Cross-framework note: ODMantic's `opportunity_amount` and `probability` do not
  carry the precision/nullable nuances that SA/ME encode (`probability` is a
  non-optional `int` defaulting to 0 in ODMantic).

## Implementation Notes

Backfill of PR #28.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/28
- https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_lead.htm
