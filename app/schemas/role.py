from datetime import datetime

from pydantic import BaseModel


# Base model for Role attributes
class RoleBase(BaseModel):
    name: str
    description: str | None = None


# Model for creating a Role
class RoleCreate(RoleBase):
    pass


# Model for updating a Role
class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


# Schema for User when included in a Role response
class UserInRole(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# Response model for Role
class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Extended response model with users
class RoleDetailResponse(RoleResponse):
    users: list[UserInRole] = []
