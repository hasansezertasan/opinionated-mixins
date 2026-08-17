# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from db import Base
from opinionated_mixins.contrib.sqlalchemy.person import Person as SQLAPerson
from sqlalchemy import Column, Integer, String


class Person(Base, SQLAPerson):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    email = Column(String(64), index=True, unique=True)
