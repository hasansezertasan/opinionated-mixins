---
rfc: "0007"
title: Activity
type: mixin
status: accepted
created: 2026-04-22
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 42
supersedes: null
superseded_by: null
---

# RFC-0007: Activity

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #42 (with a follow-up in PR #45) before this process
> existed.

## Summary

An `Activity` mixin for event-level activity records following the W3C Activity
Streams 2.0 sentence pattern — *{actor} {verb} {action_object} on {target}* —
with three polymorphic entity pairs, a visibility flag, a JSON payload, and a
creation timestamp.

## Motivation

Activity feeds ("Alice commented on Issue #5", "Bob merged PR #12") are a common
product surface. The Activity Streams model is the well-established schema for
them. Providing it as a mixin gives every model the same, interoperable event
shape rather than ad-hoc per-app audit logs.

## Research

### Field Naming

| Source | Core fields | Link |
| ------ | ----------- | ---- |
| W3C Activity Streams 2.0 | `actor`, `verb`/`type`, `object`, `target` | https://www.w3.org/TR/activitystreams-core/ |
| django-activity-stream | `actor`, `verb`, `action_object`, `target`, `public`, `timestamp`, `data` | https://django-activity-stream.readthedocs.io/ |
| Activity Streams 1.0 | `actor`, `verb`, `object`, `target` | https://web.archive.org/web/20130104020946/http://activitystrea.ms/specs/json/1.0/ |

**Chosen names.** `verb`, `actor`, `target`, `action_object`, `public`, `data`
follow django-activity-stream directly (itself an Activity Streams
implementation). Each entity is stored as a framework-agnostic polymorphic pair
(`*_type` + `*_id`) rather than a GenericForeignKey, so the shape is identical
across ORM and ODM. `created_at` names the event timestamp (django uses
`timestamp`; `created_at` was chosen for consistency with RFC-0001).

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `verb` | `str` | yes | — | `String(255)`, indexed |
| `description` | `str \| None` | no | `None` | `Text` |
| `data` | `dict \| None` | no | `None` | `JSON` |
| `actor_type` | `str` | yes | — | `String(255)`, indexed |
| `actor_id` | `str` | yes | — | `String(255)`, indexed |
| `target_type` | `str \| None` | no | `None` | `String(255)`, indexed |
| `target_id` | `str \| None` | no | `None` | `String(255)`, indexed |
| `action_object_type` | `str \| None` | no | `None` | `String(255)`, indexed |
| `action_object_id` | `str \| None` | no | `None` | `String(255)`, indexed |
| `public` | `bool` | yes | `True` | indexed |
| `created_at` | `datetime` | yes | `now(utc)` | tz-aware, indexed |

### Reference Implementation

```python
# SQLAlchemy
import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Activity:
    """Activity mixin for SQLAlchemy models.

    Event-level activity record following the W3C Activity Streams 2.0
    sentence pattern: {actor} {verb} {action_object} on {target}.
    """

    __abstract__ = True

    verb = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    actor_type = Column(String(255), nullable=False, index=True)
    actor_id = Column(String(255), nullable=False, index=True)
    target_type = Column(String(255), nullable=True, index=True)
    target_id = Column(String(255), nullable=True, index=True)
    action_object_type = Column(String(255), nullable=True, index=True)
    action_object_id = Column(String(255), nullable=True, index=True)
    public = Column(Boolean, nullable=False, index=True, default=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# MongoEngine
import datetime
from typing import Any, ClassVar

from mongoengine import BooleanField, DateTimeField, DictField, StringField


class Activity:
    """Activity mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    verb = StringField(required=True, max_length=255, index=True)
    description = StringField()
    data = DictField(default=None)
    actor_type = StringField(required=True, max_length=255, index=True)
    actor_id = StringField(required=True, max_length=255, index=True)
    target_type = StringField(max_length=255, index=True)
    target_id = StringField(max_length=255, index=True)
    action_object_type = StringField(max_length=255, index=True)
    action_object_id = StringField(max_length=255, index=True)
    public = BooleanField(required=True, default=True, index=True)
    created_at = DateTimeField(
        required=True,
        index=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

```python
# ODMantic
import datetime
from typing import Any

from odmantic import Field


class Activity:
    """Activity mixin for ODMantic models."""

    verb: str = Field(..., max_length=255)
    description: str | None = Field(default=None)
    data: dict[str, Any] | None = Field(default=None)
    actor_type: str = Field(..., max_length=255)
    actor_id: str = Field(..., max_length=255)
    target_type: str | None = Field(default=None, max_length=255)
    target_id: str | None = Field(default=None, max_length=255)
    action_object_type: str | None = Field(default=None, max_length=255)
    action_object_id: str | None = Field(default=None, max_length=255)
    public: bool = Field(default=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **GenericForeignKey (django-style)** — rejected: not portable to the ODMs;
   the `*_type`/`*_id` pair achieves the same polymorphism uniformly.
2. **Reusing the Notification shape** — rejected: notifications model
   per-recipient *delivery state*; activities model *events*. See RFC-0006.
3. **Storing the whole Activity Streams JSON blob only** — rejected: first-class
   indexed columns for actor/verb/target make feeds queryable; `data` remains
   for extras.

## Discussion Summary

Backfilled — original discussion on PRs #42 and #45. The three-pair polymorphic
model (actor required; target and action_object optional) and the `public` flag
follow django-activity-stream's design decisions.

## Consequences

- Implemented across all four contrib modules with identical field names.
- `data` in-place mutations are not tracked by SQLAlchemy (reassign to persist).
- ODMantic does not encode `index=True`.

## Implementation Notes

- PR #42 introduced the mixin; PR #45 followed up. `github_pr` records #42.
- `created_at` here is the event timestamp and is independent of the
  `CreatedAt` mixin (RFC-0001).

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/42
- https://github.com/hasansezertasan/opinionated-mixins/pull/45
- https://www.w3.org/TR/activitystreams-core/
- https://django-activity-stream.readthedocs.io/
