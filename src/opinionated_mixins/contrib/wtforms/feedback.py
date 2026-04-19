# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class Feedback:
    """Feedback mixin for WTForms forms."""

    subject = StringField(
        label="Subject",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    content = TextAreaField(
        label="Content",
        validators=[DataRequired()],
    )
    category = SelectField(
        label="Category",
        choices=[(c.value, c.value.title()) for c in FeedbackCategory],
        default=FeedbackCategory.OTHER.value,
        validators=[DataRequired()],
    )
    status = SelectField(
        label="Status",
        choices=[(c.value, c.value.title()) for c in FeedbackStatus],
        default=FeedbackStatus.PENDING.value,
        validators=[DataRequired()],
    )
