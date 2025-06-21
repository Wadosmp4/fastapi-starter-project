from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PostCategory(Base):
    """Association table for many-to-many relationship between posts and categories."""

    __tablename__ = 'post_categories'

    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: Add relationships to navigate directly from the association
    post = relationship('Post', back_populates='post_categories')
    category = relationship('Category', back_populates='post_categories')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-One: Many posts belong to one user
    author = relationship('User', back_populates='posts')

    # One-to-Many: One post can have many comments
    comments = relationship(
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan',
    )

    # Many-to-Many: Posts can have many categories (using association class)
    post_categories = relationship(
        'PostCategory',
        back_populates='post',
        cascade='all, delete-orphan',
    )
    categories = relationship('Category', secondary='post_categories', viewonly=True)
