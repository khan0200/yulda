from enum import Enum


class AutoListingType(str, Enum):
    SALE = "SALE"
    RENTAL = "RENTAL"


class FuelType(str, Enum):
    GASOLINE = "GASOLINE"
    DIESEL = "DIESEL"
    LPG = "LPG"
    HYBRID = "HYBRID"
    ELECTRIC = "ELECTRIC"


class TransmissionType(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"


class AutoListingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    UNAVAILABLE = "UNAVAILABLE"
