from opinionated_mixins.contrib.sqlalchemy.person import Person as SQLAlchemyPerson


class Person(SQLAlchemyPerson):
    """
    SQLModel `Person` document that represents a person.

    Inherits from and `opinionated_mixins.contrib.sqlalchemy.person.Person`.
    """
