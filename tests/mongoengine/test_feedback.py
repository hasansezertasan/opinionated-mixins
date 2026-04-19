# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.mongoengine import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus


class TestMongoEngineFeedback:
    def test_has_subject_field(self) -> None:
        assert hasattr(Feedback, "subject")
        assert Feedback.subject.required is True
        assert Feedback.subject.max_length == 255

    def test_has_content_field(self) -> None:
        assert hasattr(Feedback, "content")
        assert Feedback.content.required is True

    def test_has_category_field(self) -> None:
        assert hasattr(Feedback, "category")
        assert Feedback.category.required is True
        assert Feedback.category.default == FeedbackCategory.OTHER.value

    def test_category_choices(self) -> None:
        choices = Feedback.category.choices
        expected = [c.value for c in FeedbackCategory]
        assert choices == expected

    def test_has_status_field(self) -> None:
        assert hasattr(Feedback, "status")
        assert Feedback.status.required is True
        assert Feedback.status.default == FeedbackStatus.PENDING.value

    def test_status_choices(self) -> None:
        choices = Feedback.status.choices
        expected = [c.value for c in FeedbackStatus]
        assert choices == expected
