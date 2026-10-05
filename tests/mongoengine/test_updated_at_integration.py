"""Integration tests for MongoEngine UpdatedAt mixin."""

import datetime

from mongoengine import Document, StringField
from opinionated_mixins.contrib.mongoengine import UpdatedAt


class MyModel(UpdatedAt, Document):
    """Test model composing UpdatedAt with Document."""

    meta = {"collection": "test_updated_at"}
    name = StringField(required=True)


class TestUpdatedAtIntegration:
    """Test UpdatedAt mixin composition, instantiation, and roundtrip."""

    def test_updated_at_set_on_save(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded is not None
        assert loaded.updated_at is not None
        assert isinstance(loaded.updated_at, datetime.datetime)

    def test_updated_at_is_utc(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - loaded.updated_at.replace(tzinfo=datetime.timezone.utc)
        assert delta.total_seconds() < 5

    def test_updated_at_survives_roundtrip(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        # mongomock truncates microseconds; compare up to millisecond precision
        diff = loaded.updated_at - obj.updated_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01

    def test_updated_at_can_be_manually_refreshed(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        first_loaded = MyModel.objects.first()
        first_ts = first_loaded.updated_at
        # Mixin provides the field; consumer is responsible for updating it
        import time

        time.sleep(0.01)
        obj.updated_at = datetime.datetime.now(datetime.timezone.utc)
        obj.name = "changed"
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded.name == "changed"
        # Both timestamps come from mongomock with same truncation
        assert loaded.updated_at >= first_ts
