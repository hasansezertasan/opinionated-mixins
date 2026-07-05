"""Integration tests for ODMantic CreatedAt mixin."""

import datetime

import pytest
from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import CreatedAt
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(TypeError, ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


def _build_model() -> type[Model]:
    """Build the test model composing the mixin with an ODMantic ``Model``.

    This composition currently fails (see the module-level xfail). Under
    pydantic >= 2.13 the failure surfaces at *class-creation* time as a
    ``TypeError`` rather than at instantiation, so the model is built inside
    each test — where the xfail marker can catch it — instead of at import
    time, which would otherwise break test collection.
    """

    class MyModel(CreatedAt, Model):
        model_config = {"collection": "test_created_at"}
        name: str = Field(...)

    return MyModel


class TestCreatedAtIntegration:
    """Test CreatedAt mixin composition, instantiation, and roundtrip."""

    async def test_created_at_set_on_save(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded is not None
        assert loaded.created_at is not None
        assert isinstance(loaded.created_at, datetime.datetime)

    async def test_created_at_is_recent(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        now = datetime.datetime.now(datetime.timezone.utc)
        utc = datetime.timezone.utc
        delta = (now - loaded.created_at.replace(tzinfo=utc)).total_seconds()
        assert delta < 5

    async def test_created_at_survives_roundtrip(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        # mongomock may truncate microseconds; compare up to millisecond precision
        diff = loaded.created_at - obj.created_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01
