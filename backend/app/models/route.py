from enum import Enum


class RoutePostType(str, Enum):
    OFFER = "OFFER"
    """Driver posting available seats/capacity along a route."""
    REQUEST = "REQUEST"
    """Passenger/sender posting a need for a ride or small parcel along a route."""


class RouteStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    """Auto-set 1 hour after departure_at; owner can repost to reactivate."""
