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


class JobPostStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
