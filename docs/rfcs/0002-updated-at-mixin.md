---
rfc: "0002"
title: UpdatedAt
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

# RFC-0002: UpdatedAt

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #38 before this process existed.

## Summary

An `UpdatedAt` mixin providing an `updated_at` timestamp, set at insert time and
refreshed automatically on every update (where the framework supports it).

## Motivation

Last-modification time is the companion to creation time and is just as widely
needed. The subtlety worth standardising is the auto-refresh-on-update
behaviour, which differs by framework.

## Research

### Field Naming

| Source | Field name | Auto-refresh mechanism | Link |
| ------ | ---------- | ---------------------- | ---- |
| Rails ActiveRecord | `updated_at` | automatic | https://guides.rubyonrails.org/active_record_basics.html#timestamps |
| Laravel Eloquent | `updated_at` | automatic | https://laravel.com/docs/eloquent#timestamps |
| Django (`auto_now`) | conventionally `updated_at` | `auto_now=True` | https://docs.djangoproject.com/en/stable/ref/models/fields/#datefield |
| django-model-utils | `modified` | `AutoLastModifiedField` | https://django-model-utils.readthedocs.io/en/stable/models.html |

**Chosen name.** `updated_at` — matches `created_at` (RFC-0001) and the
Rails/Laravel convention. `modified` was rejected for the same consistency
reason.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `updated_at` | `datetime` | yes | `now(utc)` | tz-aware; refreshed on update in SQLAlchemy |

### Reference Implementation

```python
# SQLAlchemy
import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UpdatedAt:
    """UpdatedAt mixin for SQLAlchemy models."""

    __abstract__ = True

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# MongoEngine
import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField


class UpdatedAt:
    """UpdatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    updated_at = DateTimeField(
        required=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# ODMantic
import datetime

from odmantic import Field


class UpdatedAt:
    """UpdatedAt mixin for ODMantic models."""

    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`modified` / `last_modified` / `date_updated`** — rejected: `updated_at`
   is the dominant convention and pairs cleanly with `created_at`.
2. **Emulating `onupdate` in the ODMs** — deferred: MongoEngine and ODMantic do
   not have a native equivalent, and forcing one would require intercepting
   saves. Documented as a known gap instead (see Consequences).

## Consequences

- **Auto-refresh only in SQLAlchemy/SQLModel** via `onupdate`. In MongoEngine
  and ODMantic, `updated_at` is set on insert only; consumers must update it
  manually (e.g. in a pre-save hook). This asymmetry is intentional and
  documented rather than papered over.
- Separate from `CreatedAt` (RFC-0001) so models can opt into either.

## Implementation Notes

Backfill of PR #38. The cross-framework `onupdate` asymmetry is the main
non-obvious detail preserved here.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/38
