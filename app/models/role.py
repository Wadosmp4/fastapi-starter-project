from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(Base):
    """Association table for many-to-many relationship between users and roles."""

    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: Add relationships to navigate directly from the association
    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-Many: Roles can belong to many users (using association class)
    user_roles = relationship(
        'UserRole',
        back_populates='role',
        cascade='all, delete-orphan',
    )
    users = relationship('User', secondary='user_roles', viewonly=True)
