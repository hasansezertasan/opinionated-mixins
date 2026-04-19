# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.wtforms import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from wtforms import Form


class FeedbackForm(Feedback, Form):  # type: ignore[misc]
    pass


class TestWTFormsFeedback:
    def test_has_fields(self) -> None:
        form = FeedbackForm()
        assert "subject" in form._fields
        assert "content" in form._fields
        assert "category" in form._fields
        assert "status" in form._fields

    def test_category_choices(self) -> None:
        form = FeedbackForm()
        choice_values = [c[0] for c in form.category.choices]
        expected = [c.value for c in FeedbackCategory]
        assert choice_values == expected

    def test_category_default(self) -> None:
        form = FeedbackForm()
        assert form.category.default == FeedbackCategory.OTHER.value

    def test_status_choices(self) -> None:
        form = FeedbackForm()
        choice_values = [c[0] for c in form.status.choices]
        expected = [c.value for c in FeedbackStatus]
        assert choice_values == expected

    def test_status_default(self) -> None:
        form = FeedbackForm()
        assert form.status.default == FeedbackStatus.PENDING.value

    def test_valid_submission(self) -> None:
        form = FeedbackForm(
            data={
                "subject": "Bug report",
                "content": "Something broke",
                "category": "bug",
                "status": "pending",
            },
        )
        assert form.validate()
