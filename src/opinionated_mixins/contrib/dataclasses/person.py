import dataclasses
import datetime
from typing import Annotated

from typing_extensions import Doc


@dataclasses.dataclass
class Person:
    """Person mixin for stdlib dataclasses."""

    first_name: Annotated[str, Doc("First name of the person")]
    last_name: Annotated[str, Doc("Last name of the person")]
    middle_name: Annotated[
        str | None,
        Doc("Middle name of the person"),
    ] = dataclasses.field(default=None)
    phone_number: Annotated[
        str | None,
        Doc("Phone number of the person"),
    ] = dataclasses.field(default=None)
    email: Annotated[
        str | None,
        Doc("Email address of the person"),
    ] = dataclasses.field(default=None)
    street_address: Annotated[
        str | None,
        Doc("Street address of the person"),
    ] = dataclasses.field(default=None)
    postal_code: Annotated[
        str | None,
        Doc("Postal code of the person"),
    ] = dataclasses.field(default=None)
    city: Annotated[
        str | None,
        Doc("City of the person"),
    ] = dataclasses.field(default=None)
    country: Annotated[
        str | None,
        Doc("Country of the person (ISO 3166-1 alpha-2)"),
    ] = dataclasses.field(default=None)
    date_of_birth: Annotated[
        datetime.date | None,
        Doc("Birth date of the person"),
    ] = dataclasses.field(default=None)
    bio: Annotated[
        str | None,
        Doc("Bio of the person"),
    ] = dataclasses.field(default=None)
