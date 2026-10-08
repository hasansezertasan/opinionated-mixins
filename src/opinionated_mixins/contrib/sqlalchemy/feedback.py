from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.orm import declarative_mixin

__all__ = ["Feedback"]


@declarative_mixin
class Feedback:
    """Feedback mixin for SQLAlchemy models.

    Indexing recommendations:
    - ``subject``: index recommended if searching feedback by subject.
    - ``status``: index recommended if filtering feedback by resolution status.
    - ``category``: index recommended if querying by feedback category.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class MyFeedback(Feedback, Base):
                __tablename__ = "feedbacks"
                id = Column(Integer, primary_key=True)

                __table_args__ = (
                    Index("ix_feedbacks_subject", "subject"),
                    Index("ix_feedbacks_status", "status"),
                )
    """

    __abstract__ = True

    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(
        Enum(FeedbackCategory), nullable=False, default=FeedbackCategory.OTHER
    )
    status = Column(
        Enum(FeedbackStatus), nullable=False, default=FeedbackStatus.PENDING
    )
