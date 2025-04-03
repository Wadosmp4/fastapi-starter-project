from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentDetailResponse,
    CommentResponse,
    CommentUpdate,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Create a new comment."""
    # Check if user exists
    user = db.query(User).filter(User.id == comment.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if post exists
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    # If parent_id is provided, check if parent comment exists
    if comment.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment.parent_id).first()
        if not parent_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent comment not found",
            )

    # Create new comment
    new_comment = Comment(
        content=comment.content,
        user_id=comment.user_id,
        post_id=comment.post_id,
        parent_id=comment.parent_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/", response_model=list[CommentResponse])
def get_comments(
    skip: int = 0,
    limit: int = 100,
    post_id: int | None = None,
    user_id: int | None = None,
    parent_id: int | None = None,
    db: Session = Depends(get_db),
):
    """Get comments with optional filtering."""
    query = db.query(Comment)

    # Apply filters if provided
    if post_id:
        query = query.filter(Comment.post_id == post_id)

    if user_id:
        query = query.filter(Comment.user_id == user_id)

    if parent_id:
        query = query.filter(Comment.parent_id == parent_id)
    elif parent_id is None and not post_id and not user_id:
        # By default, return only top-level comments
        query = query.filter(Comment.parent_id is None)

    comments = query.order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    return comments


@router.get("/{comment_id}", response_model=CommentDetailResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Get a specific comment by ID with author and replies"""
    comment = (
        db.query(Comment)
        .options(joinedload(Comment.author), joinedload(Comment.replies))
        .filter(Comment.id == comment_id)
        .first()
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Format the response
    result = CommentDetailResponse.from_orm(comment)
    result.author = {
        "id": comment.author.id,
        "username": comment.author.username,
    }

    return result


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
):
    """Update a comment."""
    # Get the existing comment
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Update comment fields
    comment_data = comment_update.dict(exclude_unset=True)
    for key, value in comment_data.items():
        setattr(db_comment, key, value)

    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete a comment."""
    # Get the existing comment
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Delete the comment
    db.delete(db_comment)
    db.commit()
