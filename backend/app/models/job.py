from enum import Enum


class JobContactMethod(str, Enum):
    PHONE = "PHONE"
    """Viewer can call/dial the poster's phone number directly."""
    CHAT = "CHAT"
    """Viewer can only reach the poster via in-app messaging."""


class JobPostType(str, Enum):
    OFFER = "OFFER"
    """Employer posting an open position."""
    REQUEST = "REQUEST"
    """Worker posting that they're looking for work."""


class JobEmploymentType(str, Enum):
    PART_TIME = "PART_TIME"
    FULL_TIME = "FULL_TIME"
    DAILY = "DAILY"
    """One-off / single-day gig work."""
    CONTRACT = "CONTRACT"


class JobCategory(str, Enum):
    RESTAURANT_CAFE = "RESTAURANT_CAFE"
    RETAIL = "RETAIL"
    DELIVERY_LOGISTICS = "DELIVERY_LOGISTICS"
    CONSTRUCTION_FACTORY = "CONSTRUCTION_FACTORY"
    CLEANING = "CLEANING"
    CARE_CHILDCARE = "CARE_CHILDCARE"
    OFFICE_ADMIN = "OFFICE_ADMIN"
    IT_DESIGN = "IT_DESIGN"
    EDUCATION_TUTORING = "EDUCATION_TUTORING"
    TRANSLATION = "TRANSLATION"
    EVENT_PROMOTION = "EVENT_PROMOTION"
    OTHER = "OTHER"


class JobPayType(str, Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    PER_PROJECT = "PER_PROJECT"


class VisaType(str, Enum):
    """Korean visa categories, as commonly referenced in migrant-worker job ads."""

    E9 = "E9"
    E7 = "E7"
    H2 = "H2"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    D2 = "D2"
    D4 = "D4"
    D10 = "D10"
    G1 = "G1"
    UNDOCUMENTED = "UNDOCUMENTED"
    OTHER = "OTHER"


class HousingOption(str, Enum):
    NOT_PROVIDED = "NOT_PROVIDED"
    PROVIDED_FREE = "PROVIDED_FREE"
    PROVIDED_PAID = "PROVIDED_PAID"
    """Housing/dormitory provided but deducted from salary."""


class JobPostStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
