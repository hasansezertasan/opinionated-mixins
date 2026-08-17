#!/usr/bin/env -S uv run --script
# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
# /// script
# requires-python = ">=3.12"
# dependencies = [
# "python-dotenv",
#   "uvicorn",
#   "fastapi",
#   "fastapi-admin",
#   "redis-py",
#   "tortoise-orm",
#   "opinionated_mixins",
# ]
#
# [tool.uv.sources]
# opinionated_mixins = { path = "/Users/hasansezertasan/Developer/projects/opinionated-mixins/", editable = true }
# ///
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Model
import uvicorn

from .models import Admin, Person

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")
DB_URL = os.getenv("DB_URL")


app = FastAPI()
app.mount("/", admin_app)


@admin_app.register
class PersonResource(Model):
    label = "Person"
    model = Person
    icon = "fas fa-user"


login_provider = UsernamePasswordProvider(
    admin_model=Admin,
    login_logo_url="https://preview.tabler.io/static/logo.svg",
)


@app.on_event("startup")
async def startup() -> None:
    admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[basedir / "templates"],
        providers=[login_provider],
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
