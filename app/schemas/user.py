from datetime import datetime

from pydantic import BaseModel, EmailStr


# Base model for User attributes
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True


# Model for creating a User
class UserCreate(UserBase):
    password: str


# Model for updating a User
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None
    password: str | None = None


# Response model for User
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
