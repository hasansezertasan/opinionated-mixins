from typing import Any, ClassVar

from mongoengine import BooleanField, DateField, DecimalField, IntField, StringField

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus


class Lead:
    """Lead mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    title = StringField(required=False, max_length=255)
    salutation = StringField(required=False, max_length=64)
    job_title = StringField(required=False, max_length=255)
    company_name = StringField(required=False, max_length=255)
    website = StringField(required=False, max_length=255)
    linkedin_url = StringField(required=False, max_length=500)
    status = StringField(
        required=False,
        choices=[s.value for s in LeadStatus],
    )
    source = StringField(
        required=False,
        choices=[s.value for s in LeadSource],
    )
    industry = StringField(required=False, max_length=255)
    rating = StringField(
        required=False,
        choices=[r.value for r in LeadRating],
    )
    opportunity_amount = DecimalField(required=False, precision=2)
    currency = StringField(required=False, max_length=3)
    probability = IntField(required=False, default=0)
    close_date = DateField(required=False)
    last_contacted = DateField(required=False)
    next_follow_up = DateField(required=False)
    description = StringField(required=False)
    is_active = BooleanField(required=False, default=True)
