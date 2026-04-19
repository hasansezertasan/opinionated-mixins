# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
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
