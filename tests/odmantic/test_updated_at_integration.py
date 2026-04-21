"""Integration tests for ODMantic UpdatedAt mixin."""

import datetime

import pytest
from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import UpdatedAt
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(ValidationError, NotImplementedError),
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

    async def test_updated_at_can_be_manually_refreshed(self, mock_engine) -> None:
        obj = MyModel(name="test")
        await mock_engine.save(obj)
        first_updated = obj.updated_at
        # Mixin provides the field; consumer is responsible for updating it
        obj.updated_at = datetime.datetime.now(datetime.timezone.utc)
        obj.name = "changed"
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyModel)
        assert loaded.name == "changed"
        assert loaded.updated_at >= first_updated
