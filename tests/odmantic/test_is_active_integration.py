"""Integration tests for ODMantic IsActive mixin."""

import pytest
from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import IsActive
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

    class MyModel(IsActive, Model):
        model_config = {"collection": "test_is_active"}
        name: str = Field(...)

    return MyModel


class TestIsActiveIntegration:
    """Test IsActive mixin composition, instantiation, and roundtrip."""

    async def test_defaults_true(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded is not None
        assert loaded.is_active is True

    async def test_set_to_false(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test", is_active=False)
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.is_active is False

    async def test_update_persists(self, mock_engine) -> None:
        model_cls = _build_model()
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        obj.is_active = False
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.is_active is False
