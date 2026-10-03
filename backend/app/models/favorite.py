from enum import Enum


class FavoriteTargetType(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    COMMUNITY = "COMMUNITY"
    JOBS = "JOBS"
    SERVICES = "SERVICES"
