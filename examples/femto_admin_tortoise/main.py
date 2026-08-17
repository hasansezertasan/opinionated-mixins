#!/usr/bin/env -S uv run --script
# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "tortoise-orm",
#   "pypika",
#   "femto_admin",
#   "pydantic==2.7.0",
#   "opinionated_mixins",
# ]
#
# [tool.uv.sources]
# opinionated_mixins = { path = "/Users/hasansezertasan/Developer/projects/opinionated-mixins/", editable = true }
# femto_admin = { git = "https://github.com/XyncNet/x-admin/" }
# ///

from opinionated_mixins.contrib.tortoise.person import Person as TortoisePerson
from tortoise import fields
from tortoise_api_model.model import TsModel
from tortoise_api_model.model import User as ApiUser


import os
from pathlib import Path

from femto_admin.admin import Admin

class User(ApiUser):
    posts: fields.ReverseRelation["Post"]


class Post(TsModel):
    id: int = fields.IntField(pk=True)
    text: str = fields.CharField(4095)
    published: bool = fields.BooleanField()
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="posts",
    )
    _name = "text"


class Person(TsModel, TortoisePerson):
    id = fields.IntField(pk=True, index=True)
    first_name = fields.CharField(max_length=64, null=True)
    last_name = fields.CharField(max_length=64, null=True)
    email = fields.CharField(max_length=64, index=True, unique=True)



os.environ["DB_URL"] = "sqlite://db.sqlite3"

admin = Admin(models)

app = admin.app
