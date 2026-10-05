---
rfc: "0011"
title: Template
type: mixin
status: accepted
created: 2026-04-19
updated: 2026-04-24
author: hasansezertasan
github_issue: null
github_pr: 27
supersedes: null
superseded_by: null
---

# RFC-0011: Template

> Backfilled retroactively when the RFC process was adopted. Documents a mixin
> that shipped in PR #27 before this process existed.

## Summary

A `Template` mixin for message/content templates: a `name`, a `content` body, a
`format` (how the body is rendered), and a `type` (what channel it is for).

## Motivation

Apps that send email/SMS/push routinely store reusable templates. They share a
common shape — an identifying name, the template body, its markup format, and
the delivery channel. Standardising `format` and `type` vocabularies makes
templates portable across notification backends.

## Research

### Field Naming

| Source | Naming | Link |
| ------ | ------ | ---- |
| SendGrid templates | template `name`, `html_content`/`plain_content` | https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates |
| Mailgun templates | `name`, `template` (content) | https://documentation.mailgun.com/ |
| Twilio Content API | template with content `type` per channel | https://www.twilio.com/docs/content |

**Chosen names.** `name` + `content`; `format` for the markup (plain/HTML/
markdown) and `type` for the channel (email/SMS/push). Splitting *format* from
*channel* mirrors how SendGrid (HTML vs plain) and Twilio (per-channel content)
model them separately.

### Enum Values

| Source | Format | Type/channel |
| ------ | ------ | ------------ |
| SendGrid | HTML, plain | email |
| Markdown-based tools | markdown | — |
| Twilio / push providers | — | SMS, push |

**Chosen values.** `TemplateFormat = {PLAIN, HTML, MARKDOWN}` and
`TemplateType = {EMAIL, SMS, PUSH, OTHER}`.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `name` | `str` | yes | — | `String(255)`, indexed (SA) |
| `content` | `str` | yes | — | `Text` |
| `format` | `TemplateFormat` | yes | `PLAIN` | enum |
| `type` | `TemplateType` | yes | `OTHER` | enum |

### Enum Additions

```python
# src/opinionated_mixins/enums.py
class TemplateFormat(_AutoStrEnum):
    """Format of a template's content."""

    PLAIN = enum.auto()
    HTML = enum.auto()
    MARKDOWN = enum.auto()


class TemplateType(_AutoStrEnum):
    """Type/purpose of a template."""

    EMAIL = enum.auto()
    SMS = enum.auto()
    PUSH = enum.auto()
    OTHER = enum.auto()
```

### Reference Implementation

```python
# SQLAlchemy
from opinionated_mixins.enums import TemplateFormat, TemplateType

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Template:
    """Template mixin for SQLAlchemy models."""

    __abstract__ = True

    name = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    format = Column(Enum(TemplateFormat), nullable=False, default=TemplateFormat.PLAIN)
    type = Column(Enum(TemplateType), nullable=False, default=TemplateType.OTHER)
```

```python
# MongoEngine
from typing import Any, ClassVar

from opinionated_mixins.enums import TemplateFormat, TemplateType

from mongoengine import StringField


class Template:
    """Template mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    name = StringField(required=True, max_length=255)
    content = StringField(required=True)
    format = StringField(
        required=True,
        default=TemplateFormat.PLAIN.value,
        choices=[c.value for c in TemplateFormat],
    )
    type = StringField(
        required=True,
        default=TemplateType.OTHER.value,
        choices=[c.value for c in TemplateType],
    )
```

```python
# ODMantic
from opinionated_mixins.enums import TemplateFormat, TemplateType

from odmantic import Field


class Template:
    """Template mixin for ODMantic models."""

    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    format: TemplateFormat = Field(default=TemplateFormat.PLAIN)
    type: TemplateType = Field(default=TemplateType.OTHER)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **Combine `format` and `type` into one field** — rejected: markup format and
   delivery channel are independent (an email can be HTML or plain).
2. **Separate `subject` field** — deferred: subjects are channel-specific
   (email has one, SMS does not); left to consumers.
3. **`body` instead of `content`** — rejected for cross-mixin consistency.

## Discussion Summary

Backfilled — original discussion on PR #27. The format/channel split follows how
SendGrid and Twilio model templates.

## Consequences

- Implemented across all four contrib modules with identical field names.
- Adds two enums to `enums.py`.
- `format` and `type` shadow Python builtins as attribute names; this matches
  the domain vocabulary and is scoped to the model instance.

## Implementation Notes

Backfill of PR #27.

## References

- https://github.com/hasansezertasan/opinionated-mixins/pull/27
- https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates
