import datetime

from odmantic import Field

__all__ = ["UpdatedAt"]


class UpdatedAt:
    """UpdatedAt mixin for ODMantic models."""

    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
