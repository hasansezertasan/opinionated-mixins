# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import dataclasses
from typing import Annotated

from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from typing_extensions import Doc


@dataclasses.dataclass
class Feedback:
    """Feedback mixin for stdlib dataclasses."""

    subject: Annotated[str, Doc("Subject of the feedback")]
    content: Annotated[str, Doc("Content of the feedback")]
    category: Annotated[FeedbackCategory, Doc("Category of the feedback")] = (
        dataclasses.field(
            default=FeedbackCategory.OTHER,
        )
    )
    status: Annotated[FeedbackStatus, Doc("Status of the feedback")] = (
        dataclasses.field(
            default=FeedbackStatus.PENDING,
        )
    )
