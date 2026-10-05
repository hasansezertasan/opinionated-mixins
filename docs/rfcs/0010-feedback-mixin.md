---
rfc: "0010"
title: Feedback
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 26
supersedes: null
superseded_by: null
---

# RFC-0010: Feedback

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #26 before this process existed.

## Summary

A `Feedback` mixin: a `subject`, a `content` body, a `category` (what kind of
feedback), and a `status` (where it is in triage).

## Motivation

In-app feedback / "contact us" / feature-request widgets are common, and they
converge on the same shape: a short subject, a body, a category, and a triage
status. Standardising the category and status vocabularies makes feedback
dashboards portable.

## Research

### Field Naming

| Source | Naming | Link |
| ------ | ------ | ---- |
| GitHub issues | `title`, `body`, labels (`bug`, `enhancement`) | https://docs.github.com/en/issues |
| Zendesk tickets | `subject`, `description`, `status` | https://support.zendesk.com/ |
| Canny / feature-feedback tools | title, details, category, status | https://canny.io/ |

**Chosen names.** `subject` + `content` (Zendesk uses `subject`; `content` is
kept consistent with the other content mixins). `category` and `status` are
separate enums, matching the ticket model where *type* and *state* are
orthogonal.

### Enum Values

| Source | Category values | Status values |
| ------ | --------------- | ------------- |
| GitHub labels | bug, enhancement(→feature) | open/closed |
| Zendesk | — | new/open/pending/solved |
| Common triage | bug, feature, improvement, other | pending, reviewed, resolved, dismissed |

**Chosen values.** `FeedbackCategory = {BUG, FEATURE, IMPROVEMENT, OTHER}` and
`FeedbackStatus = {PENDING, REVIEWED, RESOLVED, DISMISSED}` — a triage lifecycle
generalised from Zendesk-style ticket states, with `DISMISSED` for "won't act".

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `subject` | `str` | yes | — | `String(255)`, indexed (SA) |
| `content` | `str` | yes | — | `Text` |
| `category` | `FeedbackCategory` | yes | `OTHER` | enum |
| `status` | `FeedbackStatus` | yes | `PENDING` | enum |

### Enum Additions

```python
# src/opinionated_mixins/enums.py
class FeedbackCategory(_AutoStrEnum):
    """Category of a feedback submission."""

    BUG = enum.auto()
    FEATURE = enum.auto()
    IMPROVEMENT = enum.auto()
    OTHER = enum.auto()


class FeedbackStatus(_AutoStrEnum):
    """Status of a feedback submission."""

    PENDING = enum.auto()
    REVIEWED = enum.auto()
    RESOLVED = enum.auto()
    DISMISSED = enum.auto()
```

### Reference Implementation

```python
# SQLAlchemy
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Feedback:
    """Feedback mixin for SQLAlchemy models."""

    __abstract__ = True

    subject = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(
        Enum(FeedbackCategory),
        nullable=False,
        default=FeedbackCategory.OTHER,
    )
    status = Column(
        Enum(FeedbackStatus),
        nullable=False,
        default=FeedbackStatus.PENDING,
    )
```

```python
# MongoEngine
from typing import Any, ClassVar

from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from mongoengine import StringField


class Feedback:
    """Feedback mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    subject = StringField(required=True, max_length=255)
    content = StringField(required=True)
    category = StringField(
        required=True,
        default=FeedbackCategory.OTHER.value,
        choices=[c.value for c in FeedbackCategory],
    )
    status = StringField(
        required=True,
        default=FeedbackStatus.PENDING.value,
        choices=[c.value for c in FeedbackStatus],
    )
```

```python
# ODMantic
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from odmantic import Field


class Feedback:
    """Feedback mixin for ODMantic models."""

    subject: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: FeedbackCategory = Field(default=FeedbackCategory.OTHER)
    status: FeedbackStatus = Field(default=FeedbackStatus.PENDING)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **Single `type` field, no `status`** — rejected: kind and triage-state are
   orthogonal; collapsing them loses the workflow dimension.
2. **`title`/`body` naming** — rejected in favour of `subject`/`content` for
   consistency with ticketing tools and the other content mixins.
3. **A numeric priority field** — deferred; not part of the common minimum.

## Discussion Summary

Backfilled — original discussion on PR #26. The two-enum (category + status)
model was chosen over a single field to keep kind and workflow-state separate.

## Consequences

- Implemented across all four contrib modules with identical field names.
- Adds two enums to `enums.py`.

## Implementation Notes

Backfill of PR #26.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/26
- https://support.zendesk.com/
