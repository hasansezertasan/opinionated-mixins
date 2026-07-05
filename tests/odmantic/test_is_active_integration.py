"""Integration tests for ODMantic IsActive mixin.

The model is built inside each test via the ``build_mixin_model`` fixture — not
at module level — because composing an ODMantic ``Model`` with a mixin parent
raises at class-creation time under pydantic >= 2.13 (see the fixture's
docstring and issue #39). Building at import time would break collection.
"""

import pytest
from opinionated_mixins.contrib.odmantic import IsActive
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(TypeError, ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class TestIsActiveIntegration:
    """Test IsActive mixin composition, instantiation, and roundtrip."""

    async def test_defaults_true(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(IsActive, "test_is_active")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded is not None
        assert loaded.is_active is True

    async def test_set_to_false(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(IsActive, "test_is_active")
        obj = model_cls(name="test", is_active=False)
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.is_active is False

    async def test_update_persists(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(IsActive, "test_is_active")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        obj.is_active = False
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.is_active is False
