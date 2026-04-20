"""Shared fixtures for MongoEngine integration tests."""

import mongoengine
import mongomock
import pytest


@pytest.fixture(autouse=True)
def _mongomock_connection():
    """Connect MongoEngine to mongomock for every test."""
    conn = mongoengine.connect(
        "testdb",
        mongo_client_class=mongomock.MongoClient,
    )
    yield conn
    mongoengine.disconnect_all()
