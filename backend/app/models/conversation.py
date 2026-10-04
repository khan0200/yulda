from enum import Enum


class ConversationListingType(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    HOUSING = "HOUSING"
    AUTO = "AUTO"
    JOBS = "JOBS"
    SERVICES = "SERVICES"
    COMMUNITY = "COMMUNITY"
