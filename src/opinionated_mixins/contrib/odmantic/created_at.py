import datetime

from odmantic import Field


class CreatedAt:
    """CreatedAt mixin for ODMantic models."""

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
