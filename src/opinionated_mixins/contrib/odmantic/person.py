from opinionated_mixins.contrib.pydantic import Person as PydanticPerson


class Person(PydanticPerson):
    """
    ODMantic `Person` model that represents a person.

    Inherits from `opinionated_mixins.contrib.pydantic.person.Person`.
    """
