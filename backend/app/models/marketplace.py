from enum import Enum


class ListingCategory(str, Enum):
    ELECTRONICS = "ELECTRONICS"
    FURNITURE = "FURNITURE"
    BIKES = "BIKES"
    CLOTHING = "CLOTHING"
    FOOD = "FOOD"
    FREE = "FREE"
    OTHER = "OTHER"


class ListingCondition(str, Enum):
    NEW = "NEW"
    USED = "USED"


class ContactMethod(str, Enum):
    PHONE = "PHONE"
    CHAT = "CHAT"
    KAKAOTALK = "KAKAOTALK"


class ListingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
