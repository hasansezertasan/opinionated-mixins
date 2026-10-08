"""Integration tests for ODMantic UpdatedAt mixin."""

import datetime

from opinionated_mixins.contrib.odmantic import UpdatedAt


class TestUpdatedAtIntegration:
    """Test UpdatedAt mixin composition, instantiation, and roundtrip."""

    async def test_updated_at_set_on_save(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(UpdatedAt, "test_updated_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded is not None
        assert loaded.updated_at is not None
        assert isinstance(loaded.updated_at, datetime.datetime)

    async def test_updated_at_is_recent(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(UpdatedAt, "test_updated_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = (now - loaded.updated_at).total_seconds()
        assert delta < 5

    async def test_updated_at_survives_roundtrip(
        self, mock_engine, build_mixin_model
    ) -> None:
        model_cls = build_mixin_model(UpdatedAt, "test_updated_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        # mongomock may truncate microseconds; compare up to millisecond precision
        diff = loaded.updated_at - obj.updated_at
        assert abs(diff.total_seconds()) < 0.01

    async def test_updated_at_can_be_manually_refreshed(
        self, mock_engine, build_mixin_model
    ) -> None:
        model_cls = build_mixin_model(UpdatedAt, "test_updated_at")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        first_updated = obj.updated_at
        # Mixin provides the field; consumer is responsible for updating it
        obj.updated_at = datetime.datetime.now(datetime.timezone.utc)
        obj.name = "changed"
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.name == "changed"
        assert loaded.updated_at >= first_updated
        assert loaded.updated_at.tzinfo == datetime.timezone.utc
