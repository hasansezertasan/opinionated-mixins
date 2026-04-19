from wtforms import DateTimeField, StringField
from wtforms.validators import DataRequired, Length, Optional


class User:
    """User mixin for WTForms forms."""

    username = StringField(
        label="Username",
        validators=[Length(min=1, max=255), DataRequired()],
    )
    email = StringField(
        label="Email",
        validators=[Length(max=254), Optional()],
    )
    date_email_verified = DateTimeField(
        label="Date Email Verified",
        validators=[Optional()],
    )
