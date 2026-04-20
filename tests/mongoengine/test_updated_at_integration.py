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
        assert (now - loaded.updated_at.replace(tzinfo=datetime.timezone.utc)).total_seconds() < 5

    def test_updated_at_survives_roundtrip(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        # mongomock truncates microseconds; compare up to millisecond precision
        assert abs((loaded.updated_at - obj.updated_at.replace(tzinfo=None)).total_seconds()) < 0.01
