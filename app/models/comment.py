from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=False,
    )
    parent_id = Column(
        Integer,
        ForeignKey('comments.id', ondelete='CASCADE'),
        nullable=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-One: Many comments belong to one user
    author = relationship('User', back_populates='comments')

    # Many-to-One: Many comments belong to one post
    post = relationship('Post', back_populates='comments')

    # Self-referential relationship: Comments can have replies
    replies = relationship(
        'Comment',
        back_populates='parent',
        cascade='all, delete-orphan',
    )
    parent = relationship('Comment', back_populates='replies', remote_side=[id])
