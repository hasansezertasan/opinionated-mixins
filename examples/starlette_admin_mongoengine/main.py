# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import os
from pathlib import Path

from dotenv import load_dotenv
from mongoengine import connect
from starlette.applications import Starlette
from starlette_admin.contrib.mongoengine import Admin, ModelView

from .models import Person

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")
MONGO_URI = os.getenv("MONGO_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")


app = Starlette()
connection = connect(host=MONGO_URI, db=MONGODB_NAME)
admin = Admin(title="MongoEngine", base_url="/")
admin.add_view(ModelView(Person, icon="fa fa-user", name="Person", label="Person"))
admin.mount_to(app)
