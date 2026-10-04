from enum import Enum


class NotificationType(str, Enum):
    NEW_MESSAGE = "NEW_MESSAGE"
    LISTING_LIKED = "LISTING_LIKED"
