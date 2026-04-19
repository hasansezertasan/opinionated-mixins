from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import Length, NumberRange, Optional

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus


class Lead:
    """Lead mixin for WTForms forms."""

    title = StringField(
        label="Title",
        validators=[Length(max=255), Optional()],
    )
    salutation = StringField(
        label="Salutation",
        validators=[Length(max=64), Optional()],
    )
    job_title = StringField(
        label="Job Title",
        validators=[Length(max=255), Optional()],
    )
    company_name = StringField(
        label="Company Name",
        validators=[Length(max=255), Optional()],
    )
    website = StringField(
        label="Website",
        validators=[Length(max=255), Optional()],
    )
    linkedin_url = StringField(
        label="LinkedIn URL",
        validators=[Length(max=500), Optional()],
    )
    status = SelectField(
        label="Status",
        choices=[(s.value, s.value) for s in LeadStatus],
        default=None,
        validators=[Optional()],
    )
    source = SelectField(
        label="Source",
        choices=[(s.value, s.value) for s in LeadSource],
        default=None,
        validators=[Optional()],
    )
    industry = StringField(
        label="Industry",
        validators=[Length(max=255), Optional()],
    )
    rating = SelectField(
        label="Rating",
        choices=[(r.value, r.value) for r in LeadRating],
        default=None,
        validators=[Optional()],
    )
    opportunity_amount = DecimalField(
        label="Opportunity Amount",
        places=2,
        validators=[Optional()],
    )
    currency = StringField(
        label="Currency",
        validators=[Length(min=3, max=3), Optional()],
    )
    probability = IntegerField(
        label="Probability",
        default=0,
        validators=[NumberRange(min=0, max=100), Optional()],
    )
    close_date = DateField(
        label="Close Date",
        validators=[Optional()],
    )
    last_contacted = DateField(
        label="Last Contacted",
        validators=[Optional()],
    )
    next_follow_up = DateField(
        label="Next Follow Up",
        validators=[Optional()],
    )
    description = TextAreaField(
        label="Description",
        validators=[Optional()],
    )
    is_active = BooleanField(
        label="Is Active",
        default=True,
    )
