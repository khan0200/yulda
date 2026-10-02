from enum import Enum


class PlaceSource(str, Enum):
    SEED = "SEED"
    USER = "USER"


class PlaceCountry(str, Enum):
    KR = "KR"
    UZ = "UZ"
    KZ = "KZ"
    KG = "KG"
    TJ = "TJ"
    TM = "TM"
    RU = "RU"
