from typing import Any, ClassVar

from opinionated_mixins.enums import TemplateFormat, TemplateType

from mongoengine import StringField


class Template:
    """Template mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    name = StringField(required=True, max_length=255)
    content = StringField(required=True)
    format = StringField(
        required=True,
        default=TemplateFormat.PLAIN.value,
        choices=[c.value for c in TemplateFormat],
    )
    type = StringField(
        required=True,
        default=TemplateType.OTHER.value,
        choices=[c.value for c in TemplateType],
    )
