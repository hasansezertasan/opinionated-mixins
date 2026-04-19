# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.enums import TemplateFormat, TemplateType

from pydantic import BaseModel, Field


class Template(BaseModel):
    """Template mixin for Pydantic models."""

    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    format: TemplateFormat = Field(default=TemplateFormat.PLAIN)
    type: TemplateType = Field(default=TemplateType.OTHER)
