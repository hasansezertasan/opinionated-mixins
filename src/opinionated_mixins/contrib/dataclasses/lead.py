import dataclasses
import datetime
from decimal import Decimal
from typing import Annotated

from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from typing_extensions import Doc


@dataclasses.dataclass
class Lead:
    """Lead mixin for stdlib dataclasses."""

    title: Annotated[
        str | None,
        Doc("Title of the customer or lead"),
    ] = dataclasses.field(default=None)
    salutation: Annotated[
        str | None,
        Doc("Salutation (e.g. Mr., Mrs., Dr.)"),
    ] = dataclasses.field(default=None)
    job_title: Annotated[
        str | None,
        Doc("Job title of the lead"),
    ] = dataclasses.field(default=None)
    company_name: Annotated[
        str | None,
        Doc("Company name of the lead"),
    ] = dataclasses.field(default=None)
    website: Annotated[
        str | None,
        Doc("Website URL of the lead"),
    ] = dataclasses.field(default=None)
    linkedin_url: Annotated[
        str | None,
        Doc("LinkedIn profile URL"),
    ] = dataclasses.field(default=None)
    status: Annotated[
        LeadStatus | None,
        Doc("Status in the sales pipeline"),
    ] = dataclasses.field(default=None)
    source: Annotated[
        LeadSource | None,
        Doc("Source channel where the lead originated"),
    ] = dataclasses.field(default=None)
    industry: Annotated[
        str | None,
        Doc("Industry of the lead"),
    ] = dataclasses.field(default=None)
    rating: Annotated[
        LeadRating | None,
        Doc("Temperature rating of the lead"),
    ] = dataclasses.field(default=None)
    opportunity_amount: Annotated[
        Decimal | None,
        Doc("Estimated opportunity value"),
    ] = dataclasses.field(default=None)
    currency: Annotated[
        str | None,
        Doc("Currency code (ISO 4217)"),
    ] = dataclasses.field(default=None)
    probability: Annotated[
        int,
        Doc("Conversion probability (0-100)"),
    ] = dataclasses.field(default=0)
    close_date: Annotated[
        datetime.date | None,
        Doc("Expected close date"),
    ] = dataclasses.field(default=None)
    last_contacted: Annotated[
        datetime.date | None,
        Doc("Date of last contact"),
    ] = dataclasses.field(default=None)
    next_follow_up: Annotated[
        datetime.date | None,
        Doc("Date of next follow-up"),
    ] = dataclasses.field(default=None)
    description: Annotated[
        str | None,
        Doc("Description of the lead"),
    ] = dataclasses.field(default=None)
    is_active: Annotated[
        bool,
        Doc("Whether the lead is active"),
    ] = dataclasses.field(default=True)
