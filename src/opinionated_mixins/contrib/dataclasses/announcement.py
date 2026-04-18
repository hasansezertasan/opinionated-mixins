# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import dataclasses

from typing_extensions import Annotated, Doc

from opinionated_mixins.enums import AnnouncementCategory


@dataclasses.dataclass
class Announcement:
    """Announcement mixin for stdlib dataclasses."""

    title: Annotated[str, Doc("Title of the announcement")]
    content: Annotated[str, Doc("Content of the announcement")]
    category: Annotated[AnnouncementCategory, Doc("Category of the announcement")] = dataclasses.field(
        default=AnnouncementCategory.GENERAL
    )
