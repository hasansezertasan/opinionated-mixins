# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import dataclasses
from typing import Annotated

from opinionated_mixins.enums import TemplateFormat, TemplateType
from typing_extensions import Doc


@dataclasses.dataclass
class Template:
    """Template mixin for stdlib dataclasses."""

    name: Annotated[str, Doc("Name of the template")]
    content: Annotated[str, Doc("Content of the template")]
    format: Annotated[TemplateFormat, Doc("Format of the template")] = dataclasses.field(
        default=TemplateFormat.PLAIN,
    )
    type: Annotated[TemplateType, Doc("Type of the template")] = dataclasses.field(
        default=TemplateType.OTHER,
    )
