---
rfc: "0003"
title: IsActive
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

# RFC-0003: IsActive

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #38 before this process existed.

## Summary

An `IsActive` mixin providing a single `is_active` boolean, defaulting to
`True` — the canonical enable/disable (and lightweight soft-delete) flag.

## Motivation

A boolean "is this record enabled?" flag is ubiquitous: deactivated users,
hidden products, disabled feature rows. Standardising the name and default
(`True`) avoids the common `active`/`enabled`/`disabled` divergence — including
the footgun of an inverted `disabled` flag.

## Research

### Field Naming

| Source | Field name | Default | Link |
| ------ | ---------- | ------- | ---- |
| Django `AbstractUser` | `is_active` | `True` | https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User.is_active |
| Django REST / DRF conventions | `is_active` | `True` | https://www.django-rest-framework.org/ |
| Laravel (common) | `is_active` / `active` | `true` | https://laravel.com/docs/eloquent |

**Chosen name.** `is_active` — Django's `AbstractUser` convention, positively
phrased (so the default is `True`, avoiding double negatives that an
`is_disabled` flag would introduce).

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `is_active` | `bool` | yes | `True` | — |

### Reference Implementation

```python
# SQLAlchemy
from sqlalchemy import Boolean, Column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IsActive:
    """IsActive mixin for SQLAlchemy models."""

    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
```

```python
# MongoEngine
from typing import Any, ClassVar

from mongoengine import BooleanField


class IsActive:
    """IsActive mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    is_active = BooleanField(required=True, default=True)
```

```python
# ODMantic
from odmantic import Field


class IsActive:
    """IsActive mixin for ODMantic models."""

    is_active: bool = Field(default=True)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`active` (no `is_` prefix)** — rejected: `is_` prefix reads as a predicate
   and matches Django.
2. **`is_disabled` / `disabled`** — rejected: inverted booleans invite bugs and
   force a `False` default.
3. **A full soft-delete `deleted_at` timestamp** — out of scope; that is a
   distinct concern and could be its own future RFC. `is_active` is the simple
   enable/disable flag.

## Consequences

- Provided in all four contrib modules with an identical field name and default.
- Not a substitute for row-level soft delete with retention timestamps; it is a
  simple boolean.

## Implementation Notes

Backfill of PR #38.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/38
- https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User.is_active
