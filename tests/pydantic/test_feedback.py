# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import pytest
from opinionated_mixins.contrib.pydantic import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from pydantic import ValidationError


class TestPydanticFeedback:
    def test_create_with_defaults(self) -> None:
        obj = Feedback(subject="Bug report", content="Something broke")
        assert obj.subject == "Bug report"
        assert obj.content == "Something broke"
        assert obj.category == FeedbackCategory.OTHER
        assert obj.status == FeedbackStatus.PENDING

    def test_create_with_explicit_values(self) -> None:
        obj = Feedback(
            subject="Feature idea",
            content="Add dark mode",
            category=FeedbackCategory.FEATURE,
            status=FeedbackStatus.REVIEWED,
        )
        assert obj.category == FeedbackCategory.FEATURE
        assert obj.status == FeedbackStatus.REVIEWED

    def test_subject_required(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(content="No subject")  # type: ignore[call-arg]

    def test_content_required(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(subject="No content")  # type: ignore[call-arg]

    def test_empty_subject_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(subject="", content="Body")

    def test_subject_max_length(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(subject="x" * 256, content="Body")

    def test_category_from_string(self) -> None:
        obj = Feedback(subject="Test", content="Body", category="bug")  # type: ignore[arg-type]
        assert obj.category == FeedbackCategory.BUG

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(subject="Test", content="Body", category="invalid")  # type: ignore[arg-type]

    def test_status_from_string(self) -> None:
        obj = Feedback(subject="Test", content="Body", status="reviewed")  # type: ignore[arg-type]
        assert obj.status == FeedbackStatus.REVIEWED

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Feedback(subject="Test", content="Body", status="invalid")  # type: ignore[arg-type]
