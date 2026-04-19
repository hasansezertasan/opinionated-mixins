from odmantic import Field


class IsActive:
    """IsActive mixin for ODMantic models."""

    is_active: bool = Field(default=True)
