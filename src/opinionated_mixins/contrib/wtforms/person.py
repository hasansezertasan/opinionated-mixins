from wtforms import DateField, EmailField, StringField
from wtforms.validators import DataRequired, Length, Optional


class Person:
    """
    WTForms `Person` form that represents a person.
    """

    first_name = StringField(
        label="First name", validators=[Length(min=1, max=64), DataRequired()]
    )
    """
    First name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    last_name = StringField(
        label="Last name", validators=[Length(min=1, max=64), DataRequired()]
    )
    """
    Last name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    middle_name = StringField(
        label="Middle name",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Middle name of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    phone = StringField(
        label="Phone",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Phone number of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    email = EmailField(
        label="Email",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Email address of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    address = StringField(
        label="Address",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Address of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    postal_code = StringField(
        label="Postal code", validators=[Length(min=1, max=64), Optional()]
    )
    """
    Postal code of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    city = StringField(
        label="City",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    City of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    country = StringField(
        label="Country",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Country of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
    date_birth = DateField(label="Birth date", validators=[Optional()], default=None)
    """
    Birth date of the person.
    """
    description = StringField(
        label="Description",
        validators=[Length(min=1, max=64), Optional()],
        default=None,
    )
    """
    Description of the person.
    Minimum length: 1 character.
    Maximum length: 64 characters.
    """
