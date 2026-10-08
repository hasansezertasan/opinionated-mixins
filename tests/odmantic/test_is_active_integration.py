"""Integration tests for ODMantic IsActive mixin."""

from opinionated_mixins.contrib.odmantic import IsActive


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
