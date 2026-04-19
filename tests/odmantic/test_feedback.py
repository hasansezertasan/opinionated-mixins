# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.odmantic import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus


class TestODManticFeedback:
    def test_has_expected_annotations(self) -> None:
        annotations = Feedback.__annotations__
        assert "subject" in annotations
        assert "content" in annotations
        assert "category" in annotations
        assert "status" in annotations

    def test_category_default(self) -> None:
        assert Feedback.category.pydantic_field_info.default == FeedbackCategory.OTHER

    def test_status_default(self) -> None:
        assert Feedback.status.pydantic_field_info.default == FeedbackStatus.PENDING
