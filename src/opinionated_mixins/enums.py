import enum


class _AutoStrEnum(str, enum.Enum):
    """Base enum that auto-generates string values from member names.

    On Python <3.11 (no ``StrEnum``), ``auto()`` with ``str, Enum`` produces
    integers instead of strings. This override ensures ``auto()`` yields the
    member name as-is (e.g. ``GENERAL`` → ``"GENERAL"``).
    """

    @staticmethod
    def _generate_next_value_(
        name: str,
        _start: int,
        _count: int,
        _last_values: list[str],
    ) -> str:
        return name


class AnnouncementCategory(_AutoStrEnum):
    """Category of an announcement."""

    GENERAL = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    SUCCESS = enum.auto()
    ERROR = enum.auto()
    MAINTENANCE = enum.auto()
    UPDATE = enum.auto()
    EVENT = enum.auto()


class TemplateFormat(_AutoStrEnum):
    """Format of a template's content."""

    PLAIN = enum.auto()
    HTML = enum.auto()
    MARKDOWN = enum.auto()


class TemplateType(_AutoStrEnum):
    """Type/purpose of a template."""

    EMAIL = enum.auto()
    SMS = enum.auto()
    PUSH = enum.auto()
    OTHER = enum.auto()


class LeadStatus(_AutoStrEnum):
    """Status of a lead in the sales pipeline."""

    ASSIGNED = enum.auto()
    IN_PROCESS = enum.auto()
    CONVERTED = enum.auto()
    RECYCLED = enum.auto()
    CLOSED = enum.auto()


class LeadSource(_AutoStrEnum):
    """Source channel where a lead originated."""

    CALL = enum.auto()
    EMAIL = enum.auto()
    EXISTING_CUSTOMER = enum.auto()
    PARTNER = enum.auto()
    PUBLIC_RELATIONS = enum.auto()
    CAMPAIGN = enum.auto()
    OTHER = enum.auto()


class LeadRating(_AutoStrEnum):
    """Temperature rating of a lead."""

    HOT = enum.auto()
    WARM = enum.auto()
    COLD = enum.auto()


class FeedbackCategory(_AutoStrEnum):
    """Category of a feedback submission."""

    BUG = enum.auto()
    FEATURE = enum.auto()
    IMPROVEMENT = enum.auto()
    OTHER = enum.auto()


class FeedbackStatus(_AutoStrEnum):
    """Status of a feedback submission."""

    PENDING = enum.auto()
    REVIEWED = enum.auto()
    RESOLVED = enum.auto()
    DISMISSED = enum.auto()
