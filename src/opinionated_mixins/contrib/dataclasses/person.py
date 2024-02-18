import datetime
from dataclasses import dataclass, field

from typing_extensions import Annotated, Doc, Optional


@dataclass
class Person:
    """
    `Person` dataclass represents a person.
    """

    first_name: Annotated[
        str,
        Doc(
            """
            First name of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ]
    last_name: Annotated[
        str,
        Doc(
            """
            Last name of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ]
    middle_name: Annotated[
        Optional[str],
        Doc(
            """
            Middle name of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    phone: Annotated[
        Optional[str],
        Doc(
            """
            Phone number of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    email: Annotated[
        Optional[str],
        Doc(
            """
            Email address of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    address: Annotated[
        Optional[str],
        Doc(
            """
            Address of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    postal_code: Annotated[
        Optional[str],
        Doc(
            """
            Postal code of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    city: Annotated[
        Optional[str],
        Doc(
            """
            City of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    country: Annotated[
        Optional[str],
        Doc(
            """
            Country of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
    date_birth: Annotated[
        Optional[datetime.date],
        Doc(
            """
            Birth date of the person.
            """
        ),
    ] = field(default=None)
    description: Annotated[
        Optional[str],
        Doc(
            """
            Description of the person.
            Minimum length: 1 character.
            Maximum length: 64 characters.
            """
        ),
    ] = field(default=None)
