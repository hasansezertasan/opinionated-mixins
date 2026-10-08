"""Integration tests for ODMantic IsActive mixin."""

from odmantic import Field, Model
from opinionated_mixins.contrib.odmantic import IsActive
import pytest
from pydantic import ValidationError


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

    async def test_concrete_model_annotation_overrides_mixin_default(self) -> None:
        class MyModel(IsActive, Model):
            model_config = {"collection": "test_is_active_required"}
            is_active: bool
            name: str = Field(...)

        with pytest.raises(ValidationError):
            MyModel(name="test")

        obj = MyModel(name="test", is_active=False)
        assert obj.is_active is False

    async def test_update_persists(self, mock_engine, build_mixin_model) -> None:
        model_cls = build_mixin_model(IsActive, "test_is_active")
        obj = model_cls(name="test")
        await mock_engine.save(obj)
        obj.is_active = False
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(model_cls)
        assert loaded.is_active is False
