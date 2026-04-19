# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
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
        Enum(FeedbackCategory), nullable=False, default=FeedbackCategory.OTHER,
    )
    status = Column(
        Enum(FeedbackStatus), nullable=False, default=FeedbackStatus.PENDING,
    )
