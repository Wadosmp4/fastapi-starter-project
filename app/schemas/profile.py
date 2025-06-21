from datetime import datetime

from pydantic import BaseModel


# Base model for Profile attributes
class ProfileBase(BaseModel):
    bio: str | None = None
    website: str | None = None
    location: str | None = None
    avatar_url: str | None = None


# Model for creating a Profile
class ProfileCreate(ProfileBase):
    user_id: int


# Model for updating a Profile
class ProfileUpdate(BaseModel):
    bio: str | None = None
    website: str | None = None
    location: str | None = None
    avatar_url: str | None = None


# Schema for User when included in a Profile response
class UserInProfile(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# Response model for Profile
class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Extended response model with user details
class ProfileDetailResponse(ProfileResponse):
    user: UserInProfile | None = None
