---
rfc: "0013"
title: User
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 29
supersedes: null
superseded_by: null
---

# RFC-0013: User

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #29 before this process existed.

## Summary

A `User` mixin providing the authentication core: a unique `username`, a
`hashed_password`, an optional unique `email`, and an optional
`date_email_verified` timestamp.

## Motivation

Nearly every application has a user/account model with the same authentication
core. Standardising these field names — and, importantly, the security-relevant
choice of storing only a `hashed_password` — keeps auth models consistent and
avoids the anti-pattern of a `password` column.

## Research

### Field Naming

| Source | Fields | Link |
| ------ | ------ | ---- |
| Django `AbstractUser` | `username`, `password` (hashed), `email`, `is_active`, `date_joined` | https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User |
| Devise (Rails) | `email`, `encrypted_password`, `confirmed_at` | https://github.com/heartcombo/devise |
| RFC 5321 (email length) | ≤ 254 | https://datatracker.ietf.org/doc/html/rfc5321 |

**Chosen names.** `username` (unique, indexed) and `email` (unique, optional)
follow Django. The password column is named `hashed_password` — more explicit
than Django's `password` and Devise's `encrypted_password` — to make the
"never store plaintext" contract obvious. `date_email_verified` mirrors Devise's
`confirmed_at`. Email verification is tracked as a nullable timestamp
(`None` = unverified), consistent with the timestamp-over-boolean pattern used
elsewhere (see RFC-0006).

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `username` | `str` | yes | — | `String(255)`, unique, indexed |
| `hashed_password` | `str` | yes | — | `String(1024)` |
| `email` | `str \| None` | no | `None` | `String(254)`, unique, indexed |
| `date_email_verified` | `datetime \| None` | no | `None` | `DateTime`; `None` = unverified |

### Reference Implementation

```python
# SQLAlchemy
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class User:
    """User mixin for SQLAlchemy models."""

    __abstract__ = True

    username = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(1024), nullable=False)
    email = Column(String(254), nullable=True, unique=True, index=True)
    date_email_verified = Column(DateTime, nullable=True)
```

```python
# MongoEngine
from typing import Any, ClassVar

from mongoengine import DateTimeField, StringField


class User:
    """User mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    username = StringField(required=True, max_length=255, unique=True)
    hashed_password = StringField(required=True, max_length=1024)
    email = StringField(required=False, max_length=254, unique=True, sparse=True)
    date_email_verified = DateTimeField(required=False)
```

```python
# ODMantic
import datetime

from odmantic import Field


class User:
    """User mixin for ODMantic models."""

    username: str = Field(..., min_length=1, max_length=255)
    hashed_password: str = Field(..., min_length=1)
    email: str | None = Field(default=None, max_length=254)
    date_email_verified: datetime.datetime | None = Field(default=None)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`password` column** — rejected: naming it `hashed_password` encodes the
   security contract in the schema itself.
2. **`is_email_verified` boolean** — rejected: a nullable timestamp records
   *when* verification happened, which is more useful.
3. **Bundling profile fields (name, avatar)** — rejected: those belong to the
   `Person` mixin (RFC-0009), which composes with `User`. Keeping `User` to the
   auth core preserves single-responsibility.

## Discussion Summary

Backfilled — original discussion on PR #29. The explicit `hashed_password`
naming and the timestamp-based email verification were the deliberate choices.

## Consequences

- Implemented across all four contrib modules with identical field names.
- **Cross-framework uniqueness gap**: SQLAlchemy/MongoEngine enforce `unique`
  on `username`/`email` (MongoEngine uses `sparse=True` for the optional email);
  **ODMantic does not encode uniqueness or indexing** — consumers must add a
  unique index there. This asymmetry is documented rather than hidden.
- Composes with `Person` (RFC-0009) for a full user profile and with the
  identity mixins (RFC-0004/0005) and timestamps (RFC-0001/0002).

## Implementation Notes

Backfill of PR #29.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/29
- https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User
