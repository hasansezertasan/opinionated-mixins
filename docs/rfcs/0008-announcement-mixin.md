---
rfc: "0008"
title: Announcement
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 22
supersedes: null
superseded_by: null
---

# RFC-0008: Announcement

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #22 before this process existed.

## Summary

An `Announcement` mixin: a `title`, a `content` body, and a `category` enum for
site-wide / in-app announcements and banners.

## Motivation

Product announcements, maintenance notices, and status banners recur across
apps and share a simple shape (headline + body + a category that drives styling
and filtering). A consensus mixin standardises the category vocabulary.

## Research

### Field Naming

| Source | Field names | Link |
| ------ | ----------- | ---- |
| Bootstrap alerts | contextual classes: `info`, `warning`, `success`, `danger` | https://getbootstrap.com/docs/5.3/components/alerts/ |
| Statuspage / incident banners | `title`, `body`, incident type (`maintenance`, …) | https://support.atlassian.com/statuspage/ |
| GitHub announcement banner | `title`/message + type | https://docs.github.com/en/enterprise-server/admin/user-management/managing-users/customizing-user-messages |

**Chosen names.** `title` + `content` (headline/body); `category` for the typed
classification. `content` (not `body`/`message`) is used consistently with the
other content-bearing mixins (Feedback, Template).

### Enum Values

| Source | Values informing the set |
| ------ | ------------------------ |
| Bootstrap alerts | info, warning, success, danger(→error) |
| Status pages | maintenance, update, event |
| General | general (default) |

**Chosen values.** `AnnouncementCategory = {GENERAL, INFO, WARNING, SUCCESS,
ERROR, MAINTENANCE, UPDATE, EVENT}` — the Bootstrap alert levels plus
status-page-style operational categories, with `GENERAL` as the neutral default.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `title` | `str` | yes | — | `String(255)`, indexed (SA) |
| `content` | `str` | yes | — | `Text` |
| `category` | `AnnouncementCategory` | yes | `GENERAL` | enum |

### Enum Additions

```python
# src/opinionated_mixins/enums.py
class AnnouncementCategory(_AutoStrEnum):
    """Category of an announcement."""

    GENERAL = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    SUCCESS = enum.auto()
    ERROR = enum.auto()
    MAINTENANCE = enum.auto()
    UPDATE = enum.auto()
    EVENT = enum.auto()
```

### Reference Implementation

```python
# SQLAlchemy
from opinionated_mixins.enums import AnnouncementCategory

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Announcement:
    """Announcement mixin for SQLAlchemy models."""

    __abstract__ = True

    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(
        Enum(AnnouncementCategory),
        nullable=False,
        default=AnnouncementCategory.GENERAL,
    )
```

```python
# MongoEngine
from typing import Any, ClassVar

from opinionated_mixins.enums import AnnouncementCategory

from mongoengine import StringField


class Announcement:
    """Announcement mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    title = StringField(required=True, max_length=255)
    content = StringField(required=True)
    category = StringField(
        required=True,
        default=AnnouncementCategory.GENERAL.value,
        choices=[c.value for c in AnnouncementCategory],
    )
```

```python
# ODMantic
from opinionated_mixins.enums import AnnouncementCategory

from odmantic import Field


class Announcement:
    """Announcement mixin for ODMantic models."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: AnnouncementCategory = Field(default=AnnouncementCategory.GENERAL)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`body`/`message` instead of `content`** — rejected for consistency with
   the other content mixins.
2. **A free-form string category** — rejected: an enum gives a stable,
   styleable vocabulary and prevents typos like `"warn"` vs `"warning"`.
3. **Separate `severity` and `kind` fields** — rejected as over-engineered for
   the common case; the single `category` covers both the Bootstrap severities
   and the operational kinds.

## Discussion Summary

Backfilled — original discussion on PR #22. The category vocabulary blends
Bootstrap alert semantics with status-page operational categories.

## Consequences

- Implemented across all four contrib modules with identical field names.
- ODMantic enforces `min_length=1` on `title`/`content`; SA/ME rely on
  `nullable=False`/`required=True` without a min-length check.

## Implementation Notes

Backfill of PR #22.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/22
- https://getbootstrap.com/docs/5.3/components/alerts/
