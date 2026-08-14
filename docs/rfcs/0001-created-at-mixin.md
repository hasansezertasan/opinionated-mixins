---
rfc: "0001"
title: CreatedAt
type: mixin
status: accepted
created: 2026-04-20
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 38
supersedes: null
superseded_by: null
---

# RFC-0001: CreatedAt

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #38 before this process existed.

## Summary

A `CreatedAt` mixin providing a single `created_at` timestamp, set once at
insert time to the current UTC instant.

## Motivation

Record-creation time is one of the most universally needed audit fields. Every
framework provides it, but under slightly different names and timezone
behaviours. Fixing the name and semantics (timezone-aware UTC, set-on-insert)
once keeps every model consistent.

## Research

### Field Naming

| Source | Field name | Link |
| ------ | ---------- | ---- |
| Rails ActiveRecord | `created_at` | https://guides.rubyonrails.org/active_record_basics.html#timestamps |
| Laravel Eloquent | `created_at` | https://laravel.com/docs/eloquent#timestamps |
| Django (`auto_now_add`) | conventionally `created_at` | https://docs.djangoproject.com/en/stable/ref/models/fields/#datefield |
| django-model-utils | `created` | https://django-model-utils.readthedocs.io/en/stable/models.html |

**Chosen name.** `created_at` — the Rails/Laravel convention, and the most
common in the wider ecosystem. `created` (django-model-utils) is the notable
minority and was rejected for consistency with `updated_at` (RFC-0002).

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `created_at` | `datetime` | yes | `now(utc)` | timezone-aware; set once on insert |

### Reference Implementation

```python
# SQLAlchemy
import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class CreatedAt:
    """CreatedAt mixin for SQLAlchemy models."""

    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# MongoEngine
import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField


class CreatedAt:
    """CreatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    created_at = DateTimeField(
        required=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# ODMantic
import datetime

from odmantic import Field


class CreatedAt:
    """CreatedAt mixin for ODMantic models."""

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`created` / `creation_time` / `date_created`** — rejected: `created_at`
   has the widest cross-framework adoption.
2. **Naive (non-tz-aware) datetime** — rejected: timezone-aware UTC avoids the
   ambiguity that naive timestamps cause across deployments.
3. **DB server-side default (`func.now()`)** — rejected: a Python-side UTC
   default is portable across all backends and matches the ODM implementations.

## Consequences

- Provided in all four contrib modules with an identical field name.
- Pairs with `UpdatedAt` (RFC-0002); the two are separate mixins so a model can
  opt into creation-time tracking without update tracking.

## Implementation Notes

Backfill of PR #38, which introduced the infrastructure mixins together. Each
mixin gets its own RFC per the one-mixin-per-RFC rule.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/38
