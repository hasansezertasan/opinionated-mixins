"""Shared fixtures for ODMantic integration tests."""

from collections.abc import Callable

import pytest
from mongomock_motor import AsyncMongoMockClient
from odmantic import AIOEngine, Field, Model


class _NullAsyncSession:
    """Async context manager replacing MongoDB sessions in mongomock tests."""

    async def __aenter__(self) -> None:
        """Return no driver session so ODMantic calls mongomock without sessions."""
        return

    async def __aexit__(self, *exc_info: object) -> None:
        """Exit the no-op session context."""


@pytest.fixture
async def mock_engine() -> AIOEngine:
    """AIOEngine backed by mongomock-motor without unsupported sessions."""
    client = AsyncMongoMockClient()

    async def start_session() -> _NullAsyncSession:
        return _NullAsyncSession()

    client.start_session = start_session
    return AIOEngine(client=client, database="testdb")


@pytest.fixture
def build_mixin_model() -> Callable[[type, str], type[Model]]:
    """Return a factory that composes an ODMantic ``Model`` with a mixin."""

    def _build(mixin: type, collection: str) -> type[Model]:
        class MyModel(mixin, Model):
            model_config = {"collection": collection}
            name: str = Field(...)

        return MyModel

    return _build
