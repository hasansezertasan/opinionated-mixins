#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mongoengine",
#     "opinionated-mixins",
#     "pydantic-settings>=2,<3",
#     "starlette<1",
#     "starlette-admin==0.17.1",
#     "uvicorn",
# ]
#
# [tool.uv.sources]
# opinionated-mixins = { path = "../..", editable = true }
# ///
"""Person mixin with MongoEngine and Starlette-Admin."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from mongoengine import Document, StringField, connect, disconnect
from opinionated_mixins.contrib.mongoengine import Person as MEPerson
from pydantic_settings import BaseSettings
from starlette.applications import Starlette
from starlette_admin.contrib.mongoengine import Admin, ModelView

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class Settings(BaseSettings):
    """Example configuration, read from environment variables."""

    host: str = "127.0.0.1"
    port: int = 8000
    mongo_uri: str = "mongodb://localhost:27017"
    mongodb_name: str = "opinionated_mixins"


settings = Settings()


class Person(Document, MEPerson):
    first_name = StringField(required=False, min_length=1, max_length=64)
    last_name = StringField(required=False, min_length=1, max_length=64)


@asynccontextmanager
async def lifespan(_app: Starlette) -> AsyncIterator[None]:
    """Connect to MongoDB while the application is running."""
    connect(host=settings.mongo_uri, db=settings.mongodb_name)
    try:
        yield
    finally:
        disconnect()


app = Starlette(lifespan=lifespan)
admin = Admin(title="MongoEngine", base_url="/")
admin.add_view(ModelView(Person, icon="fa fa-user", name="Person", label="Person"))
admin.mount_to(app)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
