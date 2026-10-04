from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.notification import NotificationType


class NotificationPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    type: NotificationType
    title: str
    body: str
    link: str | None = None
    is_read: bool = False
    created_at: datetime
