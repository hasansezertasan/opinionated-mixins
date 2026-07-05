"""Integration tests for ODMantic CreatedAt mixin.

The model is built inside each test via the ``build_mixin_model`` fixture — not
at module level — because composing an ODMantic ``Model`` with a mixin parent
raises at class-creation time under pydantic >= 2.13 (see the fixture's
docstring and issue #39). Building at import time would break collection.
"""

import datetime

import pytest
from opinionated_mixins.contrib.odmantic import CreatedAt
from pydantic import ValidationError

pytestmark = pytest.mark.xfail(
    raises=(TypeError, ValidationError, NotImplementedError),
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class TestCreatedAtIntegration:
    """Test CreatedAt mixin composition, instantiation, and roundtrip."""

    async def test_created_at_set_on_save(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(CreatedAt, "test_created_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded is not None
        assert loaded.created_at is not None
        assert isinstance(loaded.created_at, datetime.datetime)

    async def test_created_at_is_recent(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(CreatedAt, "test_created_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        now = datetime.datetime.now(datetime.timezone.utc)
        utc = datetime.timezone.utc
        delta = (now - loaded.created_at.replace(tzinfo=utc)).total_seconds()
        assert delta < 5

    async def test_created_at_survives_roundtrip(
        self,
        mock_engine,
        build_mixin_model,
    ) -> None:
        model_cls = build_mixin_model(CreatedAt, "test_created_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        # mongomock may truncate microseconds; compare up to millisecond precision
        diff = loaded.created_at - obj.created_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01
