# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import AnnouncementCategory

from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class Announcement:
    """Announcement mixin for WTForms forms."""

    title = StringField(
        label="Title",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    content = TextAreaField(
        label="Content",
        validators=[DataRequired()],
    )
    category = SelectField(
        label="Category",
        choices=[(c.value, c.value.title()) for c in AnnouncementCategory],
        default=AnnouncementCategory.GENERAL.value,
        validators=[DataRequired()],
    )
