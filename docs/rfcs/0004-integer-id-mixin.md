---
rfc: "0004"
title: IntegerID
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

# RFC-0004: IntegerID

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #38 before this process existed.

## Summary

An `IntegerID` mixin providing an auto-incrementing integer primary key named
`id`. SQL-only: the ODM modules manage their own document identifiers natively.

## Motivation

An auto-increment integer PK is the default identity strategy in virtually every
relational ORM. Providing it as a mixin lets a model declare `class Foo(IntegerID, Base)`
and get the conventional `id` without boilerplate.

## Research

### Field Naming

| Source | PK field | Strategy | Link |
| ------ | -------- | -------- | ---- |
| Rails ActiveRecord | `id` | auto-increment bigint | https://guides.rubyonrails.org/active_record_basics.html |
| Django | `id` | `AutoField` (implicit) | https://docs.djangoproject.com/en/stable/topics/db/models/#automatic-primary-key-fields |
| SQLAlchemy tutorials | `id` | `Integer, primary_key=True` | https://docs.sqlalchemy.org/en/20/orm/quickstart.html |

**Chosen name.** `id` — the universal convention across Rails, Django, and
SQLAlchemy.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `id` | `int` | yes (PK) | DB-assigned | `primary_key=True`, `autoincrement=True` |

### Reference Implementation

```python
# SQLAlchemy
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IntegerID:
    """IntegerID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
```

SQLModel re-exports the SQLAlchemy implementation. **MongoEngine and ODMantic do
not implement this mixin** — both assign an ObjectId `_id` automatically, so an
integer PK mixin would be redundant and misleading there.

## Alternatives Considered

1. **`pk` / `<model>_id` naming** — rejected: `id` is the cross-framework norm.
2. **Providing an integer-PK mixin for the ODMs too** — rejected: MongoDB's
   native `_id` (ObjectId) is the idiomatic identifier; overriding it with a
   sequential integer sacrifices distribution and is rarely wanted.
3. **A single unified ID mixin covering both int and UUID** — rejected: the two
   strategies have different trade-offs; kept as separate mixins (see RFC-0005).

## Consequences

- Available only in SQLAlchemy and SQLModel.
- A model picks exactly one identity mixin: `IntegerID` (this) or `UUIDID`
  (RFC-0005).

## Implementation Notes

Backfill of PR #38. The SQL-only scope is the key non-obvious fact preserved
here — the mixin intentionally has no MongoEngine/ODMantic counterpart.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/38
