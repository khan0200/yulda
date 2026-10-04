from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.pyobjectid import PyObjectId
from app.models.user import UserRole, VerificationStatus
from app.schemas.common import GeoPoint


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=120)
    phone: str | None = Field(default=None, max_length=32)
    roles: list[UserRole] = Field(default_factory=lambda: [UserRole.CUSTOMER])
    turnstile_token: str = Field(default="", max_length=2000)

    @field_validator("roles")
    @classmethod
    def no_admin_self_signup(cls, roles: list[UserRole]) -> list[UserRole]:
        if UserRole.ADMIN in roles:
            raise ValueError("Cannot self-assign ADMIN role")
        if not roles:
            return [UserRole.CUSTOMER]
        return roles


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    turnstile_token: str = Field(default="", max_length=2000)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    turnstile_token: str = Field(default="", max_length=2000)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class UserPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    email: EmailStr
    phone: str | None = None
    name: str
    avatar: str | None = None
    roles: list[UserRole]
    verification_status: VerificationStatus
    location: GeoPoint | None = None
    is_banned: bool = False
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    phone: str | None = Field(default=None, max_length=32)
    avatar: str | None = None
    location: GeoPoint | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class DeleteAccountRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)
