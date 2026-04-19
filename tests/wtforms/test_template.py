from opinionated_mixins.contrib.wtforms import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType
from wtforms import Form


class TemplateForm(Template, Form):  # type: ignore[misc]
    pass


class TestWTFormsTemplate:
    def test_has_fields(self) -> None:
        form = TemplateForm()
        assert "name" in form._fields
        assert "content" in form._fields
        assert "format" in form._fields
        assert "type" in form._fields

    def test_format_choices(self) -> None:
        form = TemplateForm()
        choice_values = [c[0] for c in form.format.choices]
        expected = [c.value for c in TemplateFormat]
        assert choice_values == expected

    def test_format_default(self) -> None:
        form = TemplateForm()
        assert form.format.default == TemplateFormat.PLAIN.value

    def test_type_choices(self) -> None:
        form = TemplateForm()
        choice_values = [c[0] for c in form.type.choices]
        expected = [c.value for c in TemplateType]
        assert choice_values == expected

    def test_type_default(self) -> None:
        form = TemplateForm()
        assert form.type.default == TemplateType.OTHER.value

    def test_valid_submission(self) -> None:
        form = TemplateForm(
            data={
                "name": "Welcome",
                "content": "Hello {{name}}",
                "format": "PLAIN",
                "type": "EMAIL",
            },
        )
        assert form.validate()
