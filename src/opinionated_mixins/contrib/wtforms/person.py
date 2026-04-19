# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from wtforms import DateField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class Person:
    """Person mixin for WTForms forms."""

    first_name = StringField(
        label="First Name",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    last_name = StringField(
        label="Last Name",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    middle_name = StringField(
        label="Middle Name",
        validators=[Length(max=255), Optional()],
    )
    phone_number = StringField(
        label="Phone Number",
        validators=[Length(max=20), Optional()],
    )
    email = StringField(
        label="Email",
        validators=[Length(max=254), Optional()],
    )
    street_address = StringField(
        label="Street Address",
        validators=[Length(max=255), Optional()],
    )
    postal_code = StringField(
        label="Postal Code",
        validators=[Length(max=20), Optional()],
    )
    city = StringField(
        label="City",
        validators=[Length(max=255), Optional()],
    )
    country = StringField(
        label="Country",
        validators=[Length(min=2, max=2), Optional()],
    )
    date_of_birth = DateField(
        label="Date of Birth",
        validators=[Optional()],
    )
    bio = TextAreaField(
        label="Bio",
        validators=[Optional()],
    )
