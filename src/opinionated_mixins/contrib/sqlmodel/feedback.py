from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from sqlalchemy import Text
from sqlmodel import Field


__all__ = ["Feedback"]


class Feedback:
    """Feedback mixin for SQLModel models."""

    subject: str = Field(max_length=255)
    content: str = Field(sa_type=Text)
    category: FeedbackCategory = Field(default=FeedbackCategory.OTHER)
    status: FeedbackStatus = Field(default=FeedbackStatus.PENDING)
