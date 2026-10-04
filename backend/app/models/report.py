from enum import Enum


class ReportTargetType(str, Enum):
    USER = "USER"
    MARKETPLACE = "MARKETPLACE"
    HOUSING = "HOUSING"
    AUTO = "AUTO"
    JOBS = "JOBS"
    SERVICES = "SERVICES"
    COMMUNITY = "COMMUNITY"


class ReportReason(str, Enum):
    SPAM = "SPAM"
    SCAM = "SCAM"
    INAPPROPRIATE = "INAPPROPRIATE"
    HARASSMENT = "HARASSMENT"
    FAKE_LISTING = "FAKE_LISTING"
    OTHER = "OTHER"


class ReportStatus(str, Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"
