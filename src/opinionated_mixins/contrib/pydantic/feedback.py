# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from pydantic import BaseModel, Field


class Feedback(BaseModel):
    """Feedback mixin for Pydantic models."""

    subject: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: FeedbackCategory = Field(default=FeedbackCategory.OTHER)
    status: FeedbackStatus = Field(default=FeedbackStatus.PENDING)
