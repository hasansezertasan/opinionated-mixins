import pytest
from opinionated_mixins.contrib.pydantic import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType
from pydantic import BaseModel, ValidationError


class TemplateModel(Template, BaseModel):
    pass


class TestPydanticTemplate:
    def test_create_with_defaults(self) -> None:
        obj = TemplateModel(name="Welcome", content="Hello {{name}}")
        assert obj.name == "Welcome"
        assert obj.content == "Hello {{name}}"
        assert obj.format == TemplateFormat.PLAIN
        assert obj.type == TemplateType.OTHER

    def test_create_with_explicit_values(self) -> None:
        obj = TemplateModel(
            name="Newsletter",
            content="<h1>News</h1>",
            format=TemplateFormat.HTML,
            type=TemplateType.EMAIL,
        )
        assert obj.format == TemplateFormat.HTML
        assert obj.type == TemplateType.EMAIL

    def test_name_required(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(content="No name")  # type: ignore[call-arg]

    def test_content_required(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="No content")  # type: ignore[call-arg]

    def test_empty_name_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="", content="Body")

    def test_name_max_length(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="x" * 256, content="Body")

    def test_format_from_string(self) -> None:
        obj = TemplateModel(name="Test", content="Body", format="html")  # type: ignore[arg-type]
        assert obj.format == TemplateFormat.HTML

    def test_invalid_format_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="Test", content="Body", format="invalid")  # type: ignore[arg-type]

    def test_type_from_string(self) -> None:
        obj = TemplateModel(name="Test", content="Body", type="sms")  # type: ignore[arg-type]
        assert obj.type == TemplateType.SMS

    def test_invalid_type_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="Test", content="Body", type="invalid")  # type: ignore[arg-type]
