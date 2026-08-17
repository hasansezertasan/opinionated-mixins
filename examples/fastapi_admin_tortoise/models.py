# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import datetime

from fastapi_admin.models import AbstractAdmin
from opinionated_mixins.contrib.tortoise.person import Person as TortoisePerson
from tortoise import Model, fields


class Person(Model, TortoisePerson):
    id = fields.IntField(pk=True, index=True)
    first_name = fields.CharField(max_length=64, null=True)
    last_name = fields.CharField(max_length=64, null=True)
    email = fields.CharField(max_length=64, index=True, unique=True)


class Admin(AbstractAdmin):
    last_login = fields.DatetimeField(
        description="Last Login",
        default=datetime.datetime.now,
    )
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pk}#{self.username}"
