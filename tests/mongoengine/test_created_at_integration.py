"""Integration tests for MongoEngine CreatedAt mixin."""

import datetime as dt

from mongoengine import Document, StringField
from opinionated_mixins.contrib.mongoengine import CreatedAt


class MyModel(CreatedAt, Document):
    """Test model composing CreatedAt with Document."""

    meta = {"collection": "test_created_at"}
    name = StringField(required=True)


class TestCreatedAtIntegration:
    """Test CreatedAt mixin composition, instantiation, and roundtrip."""

    def test_created_at_set_on_save(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        assert loaded is not None
        assert loaded.created_at is not None
        assert isinstance(loaded.created_at, dt.datetime)

    def test_created_at_is_utc(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        now = dt.datetime.now(dt.UTC)
        # created_at should be within last 5 seconds
        delta = now - loaded.created_at.replace(tzinfo=dt.UTC)
        assert delta.total_seconds() < 5

    def test_created_at_survives_roundtrip(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        # mongomock truncates microseconds; compare up to millisecond precision
        diff = loaded.created_at - obj.created_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01
