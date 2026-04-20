"""Integration tests for MongoEngine CreatedAt mixin."""

import datetime

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
        assert isinstance(loaded.created_at, datetime.datetime)

    def test_created_at_is_utc(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        now = datetime.datetime.now(datetime.timezone.utc)
        # created_at should be within last 5 seconds
        utc = datetime.timezone.utc
        delta = now - loaded.created_at.replace(tzinfo=utc)
        assert delta.total_seconds() < 5

    def test_created_at_survives_roundtrip(self) -> None:
        obj = MyModel(name="test")
        obj.save()
        loaded = MyModel.objects.first()
        # mongomock truncates microseconds; compare up to millisecond precision
        diff = loaded.created_at - obj.created_at.replace(tzinfo=None)
        assert abs(diff.total_seconds()) < 0.01
