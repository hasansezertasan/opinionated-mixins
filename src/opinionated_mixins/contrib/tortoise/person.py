# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from tortoise import fields


class Person:
    """TortoiseORM `Person` model that represents a person.

    !!! note
        This class does not inherit from any base class and is not meant to be used directly.

    !!! example
        How to override the `Person` model:
        ```python
        from opinionated_mixins.contrib.tortoise.person import Person as TortoisePerson
        from tortoise import Model, fields


        class Person(Model, TortoisePerson):
            id = fields.IntField(pk=True, index=True)
            first_name = fields.CharField(max_length=64, null=True)
            last_name = fields.CharField(max_length=64, null=True)
            email = fields.CharField(max_length=64, index=True, unique=True)
        ```
    """

    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64)
    middle_name = fields.CharField(max_length=64, null=True)
    phone = fields.CharField(max_length=64, null=True)
    email = fields.CharField(max_length=64)
    address = fields.CharField(max_length=64, null=True)
    postal_code = fields.CharField(max_length=64, null=True)
    city = fields.CharField(max_length=64, null=True)
    country = fields.CharField(max_length=64, null=True)
    date_birth = fields.DateField(null=True)
    description = fields.CharField(max_length=64, null=True)

    class Meta:
        abstract = True
