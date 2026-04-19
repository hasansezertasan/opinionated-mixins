# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.odmantic import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType


class TestODManticTemplate:
    def test_has_expected_annotations(self) -> None:
        annotations = Template.__annotations__
        assert "name" in annotations
        assert "content" in annotations
        assert "format" in annotations
        assert "type" in annotations

    def test_format_default(self) -> None:
        assert Template.format.pydantic_field_info.default == TemplateFormat.PLAIN

    def test_type_default(self) -> None:
        assert Template.type.pydantic_field_info.default == TemplateType.OTHER
