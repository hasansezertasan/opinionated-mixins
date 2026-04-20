"""Integration tests for ODMantic CreatedAt mixin."""

import datetime

import pytest
from odmantic import Field, Model

from opinionated_mixins.contrib.odmantic import CreatedAt


pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/TODO",
    strict=True,
)


class MyModel(CreatedAt, Model):
    """Test model composing CreatedAt with Model."""

    model_config = {"collection": "test_created_at"}
    name: str = Field(...)


class TestCreatedAtIntegration:
    """Test CreatedAt mixin composition, instantiation, and roundtrip."""

    async def test_created_at_set_on_save(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded is not None
        assert loaded.created_at is not None
        assert isinstance(loaded.created_at, datetime.datetime)

    async def test_created_at_is_recent(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = (now - loaded.created_at.replace(tzinfo=datetime.timezone.utc)).total_seconds()
        assert delta < 5

    async def test_created_at_survives_roundtrip(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        # mongomock may truncate microseconds; compare up to millisecond precision
        assert abs((loaded.created_at - obj.created_at.replace(tzinfo=None)).total_seconds()) < 0.01
