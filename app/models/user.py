from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # One-to-Many: One user can have many posts
    posts = relationship('Post', back_populates='author')

    # One-to-Many: One user can have many comments
    comments = relationship('Comment', back_populates='author')

    # Many-to-Many: Users can have many roles (using association class)
    user_roles = relationship(
        'UserRole',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    roles = relationship('Role', secondary='user_roles', viewonly=True)
