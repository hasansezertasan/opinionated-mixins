import dataclasses
import datetime
from typing import Annotated

from typing_extensions import Doc


@dataclasses.dataclass
class User:
    """User mixin for stdlib dataclasses."""

    username: Annotated[str, Doc("Unique username")]
    hashed_password: Annotated[str, Doc("Hashed password")]
    email: Annotated[
        str | None,
        Doc("Email address of the user"),
    ] = dataclasses.field(default=None)
    date_email_verified: Annotated[
        datetime.datetime | None,
        Doc("Date when email was verified"),
    ] = dataclasses.field(default=None)
