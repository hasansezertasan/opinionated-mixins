# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import TemplateFormat, TemplateType

from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class Template:
    """Template mixin for WTForms forms."""

    name = StringField(
        label="Name",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    content = TextAreaField(
        label="Content",
        validators=[DataRequired()],
    )
    format = SelectField(
        label="Format",
        choices=[(c.value, c.value.title()) for c in TemplateFormat],
        default=TemplateFormat.PLAIN.value,
        validators=[DataRequired()],
    )
    type = SelectField(
        label="Type",
        choices=[(c.value, c.value.title()) for c in TemplateType],
        default=TemplateType.OTHER.value,
        validators=[DataRequired()],
    )
