# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from mongoengine import Document, StringField
from opinionated_mixins.contrib.mongoengine.person import Person as MEPerson


class Person(Document, MEPerson):
    first_name = StringField(required=False, min_length=1, max_length=64)
    last_name = StringField(required=False, min_length=1, max_length=64)
