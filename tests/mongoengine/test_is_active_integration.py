"""Integration tests for MongoEngine IsActive mixin."""

from mongoengine import Document, StringField

from opinionated_mixins.contrib.mongoengine import IsActive


class MyModel(IsActive, Document):
    """Test model composing IsActive with Document."""

    meta = {"collection": "test_is_active"}
    name = StringField(required=True)


class TestIsActiveIntegration:
    """Test IsActive mixin composition, instantiation, and roundtrip."""

    def test_defaults_true(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded is not None
        assert loaded.is_active is True

    def test_toggle_to_false(self) -> None:
        obj = MyModel(name="test", is_active=False)
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded.is_active is False

    def test_update_persists(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        obj.is_active = False
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded.is_active is False
