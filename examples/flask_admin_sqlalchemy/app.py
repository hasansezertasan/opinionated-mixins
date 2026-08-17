# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
import os
from pathlib import Path

from db import db
from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Person

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
admin = Admin(app, url="/", template_mode="bootstrap4")
db.init_app(app)

admin.add_view(ModelView(Person, db.session))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
