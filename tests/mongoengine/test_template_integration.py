"""Integration tests for MongoEngine Template mixin."""

from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType


class MyTemplate(Template, Document):
    """Test model composing Template with Document."""

    meta = {"collection": "test_templates"}


class TestTemplateIntegration:
    """Test Template mixin composition, instantiation, and roundtrip."""

    def test_create_with_defaults(self) -> None:
        obj = MyTemplate(name="Welcome", content="Hello {{name}}")
        obj.save()
        loaded = MyTemplate.objects.first()
        assert loaded is not None
        assert loaded.name == "Welcome"
        assert loaded.content == "Hello {{name}}"
        assert loaded.format == TemplateFormat.PLAIN.value
        assert loaded.type == TemplateType.OTHER.value

    def test_create_with_explicit_values(self) -> None:
        obj = MyTemplate(
            name="Newsletter",
            content="<h1>News</h1>",
            format=TemplateFormat.HTML.value,
            type=TemplateType.EMAIL.value,
        )
        obj.save()
        loaded = MyTemplate.objects.first()
        assert loaded.format == TemplateFormat.HTML.value
        assert loaded.type == TemplateType.EMAIL.value

    def test_roundtrip_preserves_all_fields(self) -> None:
        obj = MyTemplate(
            name="Alert",
            content="# Alert",
            format=TemplateFormat.MARKDOWN.value,
            type=TemplateType.PUSH.value,
        )
        obj.save()
        loaded = MyTemplate.objects.first()
        assert loaded.name == "Alert"
        assert loaded.content == "# Alert"
        assert loaded.format == TemplateFormat.MARKDOWN.value
        assert loaded.type == TemplateType.PUSH.value
