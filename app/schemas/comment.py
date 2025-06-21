from datetime import datetime

from pydantic import BaseModel


# Base model for Comment attributes
class CommentBase(BaseModel):
    content: str


# Model for creating a Comment
class CommentCreate(CommentBase):
    user_id: int
    post_id: int
    parent_id: int | None = None


# Model for updating a Comment
class CommentUpdate(BaseModel):
    content: str | None = None


# Schema for user info in a comment
class UserInComment(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# Schema for a nested reply
class ReplyResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


# Response model for Comment
class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    parent_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Extended comment response with author and replies
class CommentDetailResponse(CommentResponse):
    author: UserInComment | None = None
    replies: list[ReplyResponse] = []
