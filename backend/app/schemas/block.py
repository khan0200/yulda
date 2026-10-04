from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId


class BlockCreate(BaseModel):
    blocked_user_id: str = Field(max_length=64)


class BlockedUserSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str
    avatar: str | None = None


class BlockPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    blocked_user: BlockedUserSummary
    created_at: datetime
