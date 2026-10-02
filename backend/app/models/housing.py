from enum import Enum


class HousingType(str, Enum):
    ONE_ROOM = "ONE_ROOM"
    TWO_ROOM = "TWO_ROOM"
    ROOMMATE = "ROOMMATE"
    APARTMENT = "APARTMENT"
    COMMERCIAL = "COMMERCIAL"


class HousingAmenity(str, Enum):
    FRIDGE = "FRIDGE"
    WASHER = "WASHER"
    AC = "AC"
    PARKING = "PARKING"


class HousingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESERVED = "RESERVED"
    RENTED = "RENTED"
