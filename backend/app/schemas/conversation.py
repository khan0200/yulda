from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.conversation import ConversationListingType


class ParticipantSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str
    avatar: str | None = None


class ConversationCreate(BaseModel):
    target_user_id: str
    listing_type: ConversationListingType | None = None
    listing_id: str | None = Field(default=None, max_length=64)
    listing_title: str | None = Field(default=None, max_length=200)


class MessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


class MessagePublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    conversation_id: PyObjectId
    sender_id: PyObjectId
    body: str
    created_at: datetime
    read_at: datetime | None = None


class ConversationPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    participants: list[ParticipantSummary]
    listing_type: ConversationListingType | None = None
    listing_id: str | None = None
    listing_title: str | None = None
    last_message_preview: str | None = None
    last_message_at: datetime | None = None
    unread_count: int = 0
    created_at: datetime
    updated_at: datetime
