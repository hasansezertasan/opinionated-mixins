import dataclasses
from typing import Annotated

from opinionated_mixins.enums import AnnouncementCategory
from typing_extensions import Doc


@dataclasses.dataclass
class Announcement:
    """Announcement mixin for stdlib dataclasses."""

    title: Annotated[str, Doc("Title of the announcement")]
    content: Annotated[str, Doc("Content of the announcement")]
    category: Annotated[AnnouncementCategory, Doc("Category of the announcement")] = (
        dataclasses.field(
            default=AnnouncementCategory.GENERAL,
        )
    )
