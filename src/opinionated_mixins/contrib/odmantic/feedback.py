from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["Feedback"]


class Feedback(metaclass=ODManticMixinMetaclass):
    """Feedback mixin for ODMantic models."""

    subject: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: FeedbackCategory = Field(default=FeedbackCategory.OTHER)
    status: FeedbackStatus = Field(default=FeedbackStatus.PENDING)
