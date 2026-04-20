"""Integration tests for ODMantic Template mixin."""

import pytest
from odmantic import Model

from opinionated_mixins.contrib.odmantic import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType


pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyTemplate(Template, Model):
    """Test model composing Template with Model."""

    model_config = {"collection": "test_templates"}


class TestTemplateIntegration:
    """Test Template mixin composition, instantiation, and roundtrip."""

    async def test_create_with_defaults(self, mock_engine) -> None:
        obj = MyTemplate(name="Welcome", content="Hello {{name}}")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyTemplate)
        assert loaded is not None
        assert loaded.name == "Welcome"
        assert loaded.content == "Hello {{name}}"
        assert loaded.format == TemplateFormat.PLAIN
        assert loaded.type == TemplateType.OTHER

    async def test_create_with_explicit_values(self, mock_engine) -> None:
        obj = MyTemplate(
            name="Newsletter",
            content="<h1>News</h1>",
            format=TemplateFormat.HTML,
            type=TemplateType.EMAIL,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyTemplate)
        assert loaded.format == TemplateFormat.HTML
        assert loaded.type == TemplateType.EMAIL

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyTemplate(
            name="Alert",
            content="# Alert",
            format=TemplateFormat.MARKDOWN,
            type=TemplateType.PUSH,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyTemplate)
        assert loaded.name == "Alert"
        assert loaded.content == "# Alert"
        assert loaded.format == TemplateFormat.MARKDOWN
        assert loaded.type == TemplateType.PUSH
