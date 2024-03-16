import datetime

from typing_extensions import Optional
from wtforms import DateField, EmailField, StringField
from wtforms.validators import DataRequired, Length


class Person:
    """
    WTForms `Person` form that represents a person.
    """

    first_name: str = StringField(  # type: ignore
        label="First name", validators=[Length(min=1, max=64), DataRequired()]
    )
    """
    First name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    last_name: str = StringField(  # type: ignore
        label="Last name", validators=[Length(min=1, max=64), DataRequired()]
    )
    """
    Last name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    middle_name: Optional[str] = StringField(  # type: ignore
        label="Middle name", validators=[Length(min=1, max=64)], default=None
    )
    """
    Middle name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    phone: Optional[str] = StringField(  # type: ignore
        label="Phone", validators=[Length(min=1, max=64)], default=None
    )
    """
    Phone number of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    email: Optional[str] = EmailField(  # type: ignore
        label="Email", validators=[Length(min=1, max=64)], default=None
    )
    """
    Email address of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    address: Optional[str] = StringField(  # type: ignore
        label="Address", validators=[Length(min=1, max=64)], default=None
    )
    """
    Address of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    postal_code: Optional[str] = StringField(  # type: ignore
        label="Postal code", validators=[Length(min=1, max=64)]
    )
    """
    Postal code of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    city: Optional[str] = StringField(  # type: ignore
        label="City", validators=[Length(min=1, max=64)], default=None
    )
    """
    City of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    country: Optional[str] = StringField(  # type: ignore
        label="Country", validators=[Length(min=1, max=64)], default=None
    )
    """
    Country of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    date_birth: Optional[datetime.date] = DateField(label="Birth date", default=None)  # type: ignore
    """
    Birth date of the person.
    """
    description: Optional[str] = StringField(  # type: ignore
        label="Description", validators=[Length(min=1, max=64)], default=None
    )
    """
    Description of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
