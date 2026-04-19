import dataclasses

from opinionated_mixins.contrib.dataclasses import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType


class TestDataclassesTemplate:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(Template)

    def test_create_with_defaults(self) -> None:
        obj = Template(name="Welcome", content="Hello {{name}}")
        assert obj.name == "Welcome"
        assert obj.content == "Hello {{name}}"
        assert obj.format == TemplateFormat.PLAIN
        assert obj.type == TemplateType.OTHER

    def test_create_with_explicit_values(self) -> None:
        obj = Template(
            name="Newsletter",
            content="<h1>News</h1>",
            format=TemplateFormat.HTML,
            type=TemplateType.EMAIL,
        )
        assert obj.format == TemplateFormat.HTML
        assert obj.type == TemplateType.EMAIL

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(Template)}
        assert fields == {"name", "content", "format", "type"}
