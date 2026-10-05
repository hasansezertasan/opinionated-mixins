---
rfc: "0005"
title: UUIDID
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

# RFC-0005: UUIDID

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #38 before this process existed.

## Summary

A `UUIDID` mixin providing a UUID primary key named `id`, defaulting to a
Python-generated `uuid4`. SQL-only, mirroring `IntegerID` (RFC-0004).

## Motivation

UUID primary keys are the standard alternative to auto-increment integers when
IDs must be non-guessable, generated client-side, or unique across shards. A
mixin gives models that choice without repeating the column definition.

## Research

### Field Naming

| Source | PK field | Default | Link |
| ------ | -------- | ------- | ---- |
| Django `UUIDField` (PK) | `id` | `default=uuid.uuid4` | https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield |
| Rails (uuid PK) | `id` | `gen_random_uuid()` | https://guides.rubyonrails.org/active_record_postgresql.html#uuid |
| SQLAlchemy `Uuid` type | `id` | `default=uuid.uuid4` | https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid |

**Chosen name & default.** `id` for consistency with `IntegerID`; `uuid.uuid4`
as the Python-side default, matching Django's documented pattern and portable
across backends (unlike DB-specific `gen_random_uuid()`).

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `id` | `uuid.UUID` | yes (PK) | `uuid.uuid4` | `primary_key=True` |

### Reference Implementation

```python
# SQLAlchemy
import uuid

from sqlalchemy import Column, Uuid
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UUIDID:
    """UUIDID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
```

SQLModel re-exports the SQLAlchemy implementation. **MongoEngine and ODMantic do
not implement this mixin** — both use a native ObjectId `_id`.

## Alternatives Considered

1. **`uuid1` / `uuid7`** — `uuid4` chosen for unpredictability; time-ordered
   UUIDs (uuid7) are a reasonable future option but were not the shipped choice.
2. **String column storing the UUID text** — rejected: SQLAlchemy's `Uuid` type
   stores natively where supported and is more efficient than a `String`.
3. **DB server-side `gen_random_uuid()`** — rejected: Python-side default is
   backend-portable.

## Consequences

- Available only in SQLAlchemy and SQLModel.
- Mutually exclusive with `IntegerID` (RFC-0004) — a model chooses one identity
  mixin.

## Implementation Notes

Backfill of PR #38. Uses SQLAlchemy 2.0's `Uuid` type (no length/timezone args).

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/38
- https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield
