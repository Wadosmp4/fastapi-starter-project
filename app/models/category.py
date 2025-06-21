from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-Many: Categories can have many posts (using association class)
    post_categories = relationship(
        'PostCategory',
        back_populates='category',
        cascade='all, delete-orphan',
    )
    posts = relationship('Post', secondary='post_categories', viewonly=True)
