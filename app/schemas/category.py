from datetime import datetime

from pydantic import BaseModel


# Base model for Category attributes
class CategoryBase(BaseModel):
    name: str
    description: str | None = None


# Model for creating a Category
class CategoryCreate(CategoryBase):
    pass


# Model for updating a Category
class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


# Schema for Post when included in a Category response
class PostInCategory(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


# Response model for Category
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Extended response model with posts
class CategoryDetailResponse(CategoryResponse):
    posts: list[PostInCategory] = []
