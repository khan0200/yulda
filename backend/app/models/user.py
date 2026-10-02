from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    COURIER = "COURIER"
    EMPLOYER = "EMPLOYER"
    WORKER = "WORKER"
    SERVICE_PROVIDER = "SERVICE_PROVIDER"
    BUSINESS = "BUSINESS"
    ADMIN = "ADMIN"


class VerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
