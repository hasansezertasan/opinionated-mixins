"""Shared fixtures for ODMantic integration tests."""

import pytest
from mongomock_motor import AsyncMongoMockClient
from odmantic import AIOEngine


@pytest.fixture
async def mock_engine() -> AIOEngine:
    """AIOEngine backed by mongomock-motor."""
    client = AsyncMongoMockClient()
    return AIOEngine(client=client, database="testdb")
