---
rfc: "0006"
title: Notification
type: mixin
status: accepted
created: 2026-04-22
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 43
supersedes: null
superseded_by: null
---

# RFC-0006: Notification

> Backfilled retroactively when the RFC process was adopted. It documents a
> mixin that shipped in PR #43 (with a follow-up in PR #46) before this process
> existed. The reference implementation below is the accepted design.

## Summary

A `Notification` mixin providing per-recipient notification state: a typed,
levelled message with seen/read/archived timestamps, an actor reference for the
entity that triggered it, an optional grouping key, and a free-form JSON
payload. It deliberately omits the recipient reference — each consumer adds that
with its own framework's idioms.

## Motivation

Almost every application needs an in-app notification feed: "someone replied to
your comment", "your order shipped". These records share a near-universal shape
across platforms (a type, a severity level, read/unread state, a link to act
on). Re-implementing that shape per project produces inconsistent field names
and subtly different read-state semantics. A consensus mixin fixes the shape
once.

## Research

### Field Naming

| Source | Field names used | Link |
| ------ | ---------------- | ---- |
| django-notifications-hq | `actor`, `verb`, `level`, `unread`, `timestamp`, `description`, `data` | https://github.com/django-notifications/django-notifications |
| `noticed` (Rails) | `recipient`, `type`, `params`, `read_at`, `seen_at` | https://github.com/excid3/noticed |
| GitHub Notifications API | `reason`, `subject`, `updated_at`, `last_read_at` | https://docs.github.com/en/rest/activity/notifications |
| Web Notifications API | `title`, `body`, `data` | https://developer.mozilla.org/en-US/docs/Web/API/Notification |

**Chosen names.** `title` + `description` follow the Web Notifications API
(`title`/`body`) adapted to the project's preference for `description`. The
`seen_at`/`read_at` split (feed-appearance vs. opened) comes from `noticed` and
Facebook's notification model — a distinction django-notifications collapses
into a single `unread` flag. Nullable timestamps (`None` = not-yet) are
preferred over booleans because they record *when* the transition happened.
`group_key` mirrors Android's notification grouping. `actor_type`/`actor_id`
generalise django-notifications' `actor` GenericForeignKey to a
framework-agnostic polymorphic pair.

### Enum Values

| Source | Field | Values |
| ------ | ----- | ------ |
| django-notifications-hq | `level` | success, info, warning, error |
| Bootstrap alerts | severity | success, info, warning, danger |
| syslog / RFC 5424 | severity | info … critical … |

**Chosen values.** `NotificationLevel = {INFO, SUCCESS, WARNING, ERROR, CRITICAL}`
— django-notifications' four levels plus `CRITICAL` from syslog severity, for
notifications that must not be missed.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `notification_type` | `str` | yes | — | `String(255)`, indexed; dot-notation id (`comment.reply`) |
| `level` | `NotificationLevel` | yes | `INFO` | enum, indexed |
| `title` | `str` | yes | — | `String(255)` |
| `description` | `str \| None` | no | `None` | `Text` |
| `data` | `dict \| None` | no | `None` | `JSON` payload |
| `actor_type` | `str` | yes | — | `String(255)`, indexed |
| `actor_id` | `str` | yes | — | `String(255)`, indexed |
| `action_url` | `str \| None` | no | `None` | `String(2048)` |
| `group_key` | `str \| None` | no | `None` | `String(255)`, indexed |
| `seen_at` | `datetime \| None` | no | `None` | tz-aware, indexed; `None` = unseen |
| `read_at` | `datetime \| None` | no | `None` | tz-aware, indexed; `None` = unread |
| `archived_at` | `datetime \| None` | no | `None` | tz-aware, indexed; `None` = not archived |
| `created_at` | `datetime` | yes | `now(utc)` | tz-aware, indexed |

### Enum Additions

```python
# src/opinionated_mixins/enums.py
class NotificationLevel(_AutoStrEnum):
    """Severity/criticality level of a notification."""

    INFO = enum.auto()
    SUCCESS = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()
    CRITICAL = enum.auto()
```

### Reference Implementation

```python
# SQLAlchemy
import datetime

from opinionated_mixins.enums import NotificationLevel

from sqlalchemy import JSON, Column, DateTime, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Notification:
    """Notification mixin for SQLAlchemy models.

    Note: Does not include recipient reference. Each contrib implementation
    should add recipient/recipient_id using its framework's idioms.
    """

    __abstract__ = True

    notification_type = Column(String(255), nullable=False, index=True)
    level = Column(
        Enum(NotificationLevel),
        nullable=False,
        index=True,
        default=NotificationLevel.INFO,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    actor_type = Column(String(255), nullable=False, index=True)
    actor_id = Column(String(255), nullable=False, index=True)
    action_url = Column(String(2048), nullable=True)
    group_key = Column(String(255), nullable=True, index=True)
    seen_at = Column(DateTime(timezone=True), nullable=True, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True, index=True)
    archived_at = Column(DateTime(timezone=True), nullable=True, index=True)
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

from opinionated_mixins.enums import NotificationLevel

from mongoengine import DateTimeField, DictField, StringField


class Notification:
    """Notification mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    notification_type = StringField(required=True, max_length=255, index=True)
    level = StringField(
        required=True,
        default=NotificationLevel.INFO.value,
        choices=[level.value for level in NotificationLevel],
        index=True,
    )
    title = StringField(required=True, max_length=255)
    description = StringField()
    data = DictField()
    actor_type = StringField(required=True, max_length=255, index=True)
    actor_id = StringField(required=True, max_length=255, index=True)
    action_url = StringField(max_length=2048)
    group_key = StringField(max_length=255, index=True)
    seen_at = DateTimeField(index=True)
    read_at = DateTimeField(index=True)
    archived_at = DateTimeField(index=True)
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

from opinionated_mixins.enums import NotificationLevel

from odmantic import Field


class Notification:
    """Notification mixin for ODMantic models."""

    notification_type: str = Field(..., max_length=255)
    level: NotificationLevel = Field(default=NotificationLevel.INFO)
    title: str = Field(..., max_length=255)
    description: str | None = Field(default=None)
    data: dict[str, Any] | None = Field(default=None)
    actor_type: str = Field(..., max_length=255)
    actor_id: str = Field(..., max_length=255)
    action_url: str | None = Field(default=None, max_length=2048)
    group_key: str | None = Field(default=None, max_length=255)
    seen_at: datetime.datetime | None = Field(default=None)
    read_at: datetime.datetime | None = Field(default=None)
    archived_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **Single `is_read` boolean** — rejected: loses *when* it was read, and cannot
   express the seen-vs-read distinction.
2. **Embed a recipient FK in the mixin** — rejected: the recipient's type and
   key differ per app (User table, tenant-scoped, etc.); forcing one shape would
   break composability. Consumers add it.
3. **`verb`/`object`/`target` (Activity Streams shape)** — rejected for
   notifications: that models *events*, not per-recipient delivery state. See
   RFC-0007 (Activity), which uses that shape for its own purpose.

## Discussion Summary

Backfilled — the original design discussion lived on PR #43 and its follow-up
PR #46. Key outcome preserved here: the actor reference (`actor_type`/`actor_id`)
was made **required** in #46 (a breaking change from the initial #43 shape), on
the grounds that a notification without a triggering actor is not meaningful.

## Consequences

- All four contrib modules implement the mixin with identical field names.
- Consumers **must** add a recipient reference; the mixin is not usable alone
  for delivery without it.
- `data` in-place dict mutations are not tracked by SQLAlchemy — reassign the
  whole object to trigger change detection.
- ODMantic does not encode `index=True`; indexing is advisory in that module.

## Implementation Notes

- PR #43 introduced the mixin; PR #46 made `actor_type`/`actor_id` required
  (breaking). `github_pr` records the introducing PR (#43).
- `created_at` uses a timezone-aware UTC default via `lambda`/`default_factory`
  rather than a DB server-side default, for portability across backends.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/43
- https://github.com/hasansezertasan/opinionated-mixins/pull/46
- https://github.com/django-notifications/django-notifications
- https://github.com/excid3/noticed
