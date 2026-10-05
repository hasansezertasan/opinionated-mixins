"""Shared fixtures for ODMantic integration tests."""

from collections.abc import Callable

import pytest
from mongomock_motor import AsyncMongoMockClient
from odmantic import AIOEngine, Field, Model


@pytest.fixture
async def mock_engine() -> AIOEngine:
    """AIOEngine backed by mongomock-motor."""
    client = AsyncMongoMockClient()
    return AIOEngine(client=client, database="testdb")


@pytest.fixture
def build_mixin_model() -> Callable[[type, str], type[Model]]:
    """Return a factory that composes an ODMantic ``Model`` with a mixin.

    Composing a ``Model`` with a mixin parent currently fails (issue #39:
    ODMantic's metaclass does not process annotations inherited from mixin
    parents). Under pydantic >= 2.13 that failure surfaces at *class-creation*
    time as ``TypeError`` rather than at instantiation.

    The model must therefore be built *inside the test body* — by calling the
    returned factory — so the exception is raised during the test's call phase,
    where the strict ``xfail`` marker can catch it. Building the class at import
    time (module level) would instead raise during collection and break the
    whole test run.
    """

    def _build(mixin: type, collection: str) -> type[Model]:
        class MyModel(mixin, Model):
            model_config = {"collection": collection}
            name: str = Field(...)

        return MyModel

    return _build
