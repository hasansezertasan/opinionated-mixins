import enum


class AnnouncementCategory(str, enum.Enum):
    """Category of an announcement."""

    GENERAL = "general"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    UPDATE = "update"
    EVENT = "event"


class TemplateFormat(str, enum.Enum):
    """Format of a template's content."""

    PLAIN = "plain"
    HTML = "html"
    MARKDOWN = "markdown"


class TemplateType(str, enum.Enum):
    """Type/purpose of a template."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    OTHER = "other"


class LeadStatus(str, enum.Enum):
    """Status of a lead in the sales pipeline."""

    ASSIGNED = "assigned"
    IN_PROCESS = "in_process"
    CONVERTED = "converted"
    RECYCLED = "recycled"
    CLOSED = "closed"


class LeadSource(str, enum.Enum):
    """Source channel where a lead originated."""

    CALL = "call"
    EMAIL = "email"
    EXISTING_CUSTOMER = "existing_customer"
    PARTNER = "partner"
    PUBLIC_RELATIONS = "public_relations"
    CAMPAIGN = "campaign"
    OTHER = "other"


class LeadRating(str, enum.Enum):
    """Temperature rating of a lead."""

    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class FeedbackCategory(str, enum.Enum):
    """Category of a feedback submission."""

    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    OTHER = "other"


class FeedbackStatus(str, enum.Enum):
    """Status of a feedback submission."""

    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"
