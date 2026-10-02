from enum import Enum


class CargoPostType(str, Enum):
    OFFER = "OFFER"
    """Traveler/courier posting available cargo capacity on an international route."""
    REQUEST = "REQUEST"
    """Sender posting a need to ship something internationally."""


class CargoStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class CargoCategory(str, Enum):
    DOCUMENTS = "DOCUMENTS"
    MEDICINE = "MEDICINE"
    PERSONAL_ITEMS = "PERSONAL_ITEMS"
    FOOD = "FOOD"
    CLOTHING = "CLOTHING"
    ELECTRONICS = "ELECTRONICS"
    PHONE = "PHONE"
    LAPTOP = "LAPTOP"
    GAME_CONSOLE = "GAME_CONSOLE"
    PERFUME = "PERFUME"
    OTHER = "OTHER"
