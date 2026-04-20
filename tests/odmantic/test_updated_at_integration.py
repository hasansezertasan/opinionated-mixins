"""Integration tests for ODMantic UpdatedAt mixin."""

import datetime

import pytest
from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import UpdatedAt

pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyModel(UpdatedAt, Model):
    """Test model composing UpdatedAt with Model."""

    model_config = {"collection": "test_updated_at"}
    name: str = Field(...)


class TestUpdatedAtIntegration:
    """Test UpdatedAt mixin composition, instantiation, and roundtrip."""

    async def test_updated_at_set_on_save(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded is not None
        assert loaded.updated_at is not None
        assert isinstance(loaded.updated_at, datetime.datetime)

    async def test_updated_at_is_recent(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        now = datetime.datetime.now(datetime.timezone.utc)
        utc = datetime.timezone.utc
        delta = (now - loaded.updated_at.replace(tzinfo=utc)).total_seconds()
        assert delta < 5

    async def test_updated_at_survives_roundtrip(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        # mongomock may truncate microseconds; compare up to millisecond precision
        diff = loaded.updated_at - obj.updated_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01
