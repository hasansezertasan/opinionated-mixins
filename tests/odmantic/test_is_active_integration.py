"""Integration tests for ODMantic IsActive mixin."""

import pytest
from odmantic import Field, Model

from opinionated_mixins.contrib.odmantic import IsActive


pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyModel(IsActive, Model):
    """Test model composing IsActive with Model."""

    model_config = {"collection": "test_is_active"}
    name: str = Field(...)


class TestIsActiveIntegration:
    """Test IsActive mixin composition, instantiation, and roundtrip."""

    async def test_defaults_true(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded is not None
        assert loaded.is_active is True

    async def test_set_to_false(self, mock_engine) -> None:
        obj = MyModel(name="test", is_active=False)
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded.is_active is False

    async def test_update_persists(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        obj.is_active = False
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded.is_active is False
