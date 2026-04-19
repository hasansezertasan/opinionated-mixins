# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import enum


class AnnouncementCategory(str, enum.Enum):
    """Category of an announcement."""

    GENERAL = "general"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    UPDATE = "update"
    EVENT = "event"


class TemplateFormat(str, enum.Enum):
    """Format of a template's content."""

    PLAIN = "plain"
    HTML = "html"
    MARKDOWN = "markdown"


class TemplateType(str, enum.Enum):
    """Type/purpose of a template."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    OTHER = "other"


class FeedbackCategory(str, enum.Enum):
    """Category of a feedback submission."""

    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    OTHER = "other"


class FeedbackStatus(str, enum.Enum):
    """Status of a feedback submission."""

    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"
