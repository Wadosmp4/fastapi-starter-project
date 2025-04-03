from datetime import datetime

from pydantic import BaseModel


# Base model for Post attributes
class PostBase(BaseModel):
    title: str
    content: str


# Model for creating a Post
class PostCreate(PostBase):
    user_id: int


# Model for updating a Post
class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


# Schema for Category when included in a Post response
class CategoryInPost(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Response model for Post
class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None
    categories: list[CategoryInPost] = []

    class Config:
        from_attributes = True


# Extended response model with author details
class PostDetailResponse(PostResponse):
    author: dict | None = None
