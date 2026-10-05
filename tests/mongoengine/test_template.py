from opinionated_mixins.contrib.mongoengine import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType


class TestMongoEngineTemplate:
    def test_has_name_field(self) -> None:
        assert hasattr(Template, "name")
        assert Template.name.required is True
        assert Template.name.max_length == 255

    def test_has_content_field(self) -> None:
        assert hasattr(Template, "content")
        assert Template.content.required is True

    def test_has_format_field(self) -> None:
        assert hasattr(Template, "format")
        assert Template.format.required is True
        assert Template.format.default == TemplateFormat.PLAIN.value

    def test_format_choices(self) -> None:
        choices = Template.format.choices
        expected = [c.value for c in TemplateFormat]
        assert choices == expected

    def test_has_type_field(self) -> None:
        assert hasattr(Template, "type")
        assert Template.type.required is True
        assert Template.type.default == TemplateType.OTHER.value

    def test_type_choices(self) -> None:
        choices = Template.type.choices
        expected = [c.value for c in TemplateType]
        assert choices == expected
