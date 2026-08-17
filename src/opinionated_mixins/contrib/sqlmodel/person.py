# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from opinionated_mixins.contrib.sqlalchemy import Person as SQLAlchemyPerson


class Person(SQLAlchemyPerson):
    """SQLModel `Person` document that represents a person.

    Inherits from and `opinionated_mixins.contrib.sqlalchemy.person.Person`.
    """
