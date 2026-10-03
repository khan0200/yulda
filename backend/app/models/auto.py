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


class BodyType(str, Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    HATCHBACK = "HATCHBACK"
    WAGON = "WAGON"
    MINIVAN = "MINIVAN"
    PICKUP = "PICKUP"
    COUPE = "COUPE"
    CONVERTIBLE = "CONVERTIBLE"
    VAN = "VAN"


class AccidentHistory(str, Enum):
    NONE = "NONE"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
