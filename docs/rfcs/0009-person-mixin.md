---
rfc: "0009"
title: Person
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 25
supersedes: null
superseded_by: null
---

# RFC-0009: Person

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #25 before this process existed.

## Summary

A `Person` mixin bundling the common personal/contact/address fields: names,
phone, email, postal address, date of birth, and a bio.

## Motivation

Contact and identity records ("customer", "patient", "employee") share a large
common core. Standardising the field names and sizes (e.g. email length, ISO
country code) once avoids the drift that otherwise appears in every project.

## Research

### Field Naming

| Source | Naming | Link |
| ------ | ------ | ---- |
| Schema.org `Person` | `givenName`, `familyName`, `additionalName`, `telephone`, `email`, `birthDate`, `address` | https://schema.org/Person |
| vCard (RFC 6350) | N (family; given; additional), TEL, EMAIL, BDAY, ADR | https://datatracker.ietf.org/doc/html/rfc6350 |
| Django / web-app convention | `first_name`, `last_name`, `email` | https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User |
| RFC 5321 (email length) | local+domain ≤ 254 | https://datatracker.ietf.org/doc/html/rfc5321 |

**Chosen names.** `first_name`/`middle_name`/`last_name` (the Django/web-app
convention) rather than Schema.org's `givenName`/`familyName` — the former is
far more common in application code. `email` capped at 254 (RFC 5321).
`country` is a 2-char ISO 3166-1 alpha-2 code. `date_of_birth` and `bio` round
out the profile.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `first_name` | `str` | yes | — | `String(255)` |
| `last_name` | `str` | yes | — | `String(255)` |
| `middle_name` | `str \| None` | no | `None` | `String(255)` |
| `phone_number` | `str \| None` | no | `None` | `String(20)` |
| `email` | `str \| None` | no | `None` | `String(254)` |
| `street_address` | `str \| None` | no | `None` | `String(255)` |
| `postal_code` | `str \| None` | no | `None` | `String(20)` |
| `city` | `str \| None` | no | `None` | `String(255)` |
| `country` | `str \| None` | no | `None` | `String(2)` (ISO 3166-1 alpha-2) |
| `date_of_birth` | `date \| None` | no | `None` | `Date` |
| `bio` | `str \| None` | no | `None` | `Text` |

### Reference Implementation

```python
# SQLAlchemy
from sqlalchemy import Column, Date, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Person:
    """Person mixin for SQLAlchemy models."""

    __abstract__ = True

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(254), nullable=True)
    street_address = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(2), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)
```

```python
# MongoEngine
from typing import Any, ClassVar

from mongoengine import DateField, StringField


class Person:
    """Person mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    first_name = StringField(required=True, max_length=255)
    last_name = StringField(required=True, max_length=255)
    middle_name = StringField(required=False, max_length=255)
    phone_number = StringField(required=False, max_length=20)
    email = StringField(required=False, max_length=254)
    street_address = StringField(required=False, max_length=255)
    postal_code = StringField(required=False, max_length=20)
    city = StringField(required=False, max_length=255)
    country = StringField(required=False, max_length=2)
    date_of_birth = DateField(required=False)
    bio = StringField(required=False)
```

```python
# ODMantic
import datetime

from odmantic import Field


class Person:
    """Person mixin for ODMantic models."""

    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    street_address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: datetime.date | None = Field(default=None)
    bio: str | None = Field(default=None)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **Schema.org `givenName`/`familyName`** — rejected: `first_name`/`last_name`
   dominates application code and ORMs.
2. **A single `full_name` field** — rejected: separate name parts are needed for
   sorting, salutations, and search.
3. **A structured/embedded address object** — rejected: flat address columns are
   simpler and portable across relational and document stores; a normalised
   address model can be a separate concern.

## Discussion Summary

Backfilled — original discussion on PR #25. Column sizes (email 254, country 2,
phone 20) were chosen from the relevant standards.

## Consequences

- Implemented across all four contrib modules with identical field names.
- ODMantic uniquely enforces `min_length=2` on `country`; SA/ME cap length only.
- The mixin is intentionally "personal core" — apps add domain-specific fields.

## Implementation Notes

Backfill of PR #25.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/25
- https://schema.org/Person
- https://datatracker.ietf.org/doc/html/rfc5321
