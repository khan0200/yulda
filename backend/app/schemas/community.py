from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.community import PostCategory
from app.schemas.common import GeoPoint


class AuthorSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str
    avatar: str | None = None


class PostCreate(BaseModel):
    category: PostCategory
    title: str = Field(min_length=1, max_length=150)
    body: str = Field(min_length=1, max_length=5000)
    photos: list[str] = Field(default_factory=list, max_length=9)
    city: str | None = Field(default=None, max_length=100)
    location: GeoPoint | None = None


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    body: str | None = Field(default=None, min_length=1, max_length=5000)
    photos: list[str] | None = Field(default=None, max_length=9)
    category: PostCategory | None = None


class PostPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    category: PostCategory
    title: str
    body: str
    photos: list[str]
    city: str | None = None
    location: GeoPoint | None = None
    author: AuthorSummary
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


class CommentPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    post_id: PyObjectId
    body: str
    author: AuthorSummary
    created_at: datetime
