from enum import Enum


class ServiceCategory(str, Enum):
    BEAUTY = "BEAUTY"
    REPAIR = "REPAIR"
    TUTORING = "TUTORING"
    CLEANING = "CLEANING"
    MOVING = "MOVING"
    PET_CARE = "PET_CARE"
    PHOTOGRAPHY = "PHOTOGRAPHY"
    DESIGN = "DESIGN"
    TRANSLATION = "TRANSLATION"
    LEGAL_ADMIN = "LEGAL_ADMIN"
    EVENT = "EVENT"
    OTHER = "OTHER"


class ServiceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    UNAVAILABLE = "UNAVAILABLE"
