#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "odmantic==1.1.0",
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
"""Person fields with ODMantic and Starlette-Admin."""

from __future__ import annotations

import datetime  # noqa: TC003 - ODMantic resolves annotations at runtime.
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Field, Model
from pydantic_settings import BaseSettings
from starlette.applications import Starlette
from starlette_admin.contrib.odmantic import Admin, ModelView

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class Settings(BaseSettings):
    """Example configuration, read from environment variables."""

    host: str = "127.0.0.1"
    port: int = 8000
    mongo_uri: str = "mongodb://localhost:27017"
    mongodb_name: str = "opinionated_mixins"


settings = Settings()


class Person(Model):
    # ODMantic does not collect fields from plain mixin parents (issue #39).
    # Declare the Person fields directly; BSON dates use datetime here.
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    middle_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    street_address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: datetime.datetime | None = Field(default=None)
    bio: str | None = Field(default=None)


engine = AIOEngine(
    client=AsyncIOMotorClient(settings.mongo_uri), database=settings.mongodb_name
)


@asynccontextmanager
async def lifespan(_app: Starlette) -> AsyncIterator[None]:
    """Close the MongoDB client when the application stops."""
    try:
        yield
    finally:
        engine.client.close()


app = Starlette(lifespan=lifespan)
admin = Admin(engine=engine, title="ODMantic", base_url="/")
admin.add_view(ModelView(Person, icon="fa fa-user", name="Person", label="Person"))
admin.mount_to(app)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
