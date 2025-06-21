from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import comment_controller
from app.database import get_db
from app.exceptions import NotFoundException, to_http_exception
from app.schemas.comment import (
    CommentCreate,
    CommentDetailResponse,
    CommentResponse,
    CommentUpdate,
)


router = APIRouter(prefix='/comments', tags=['comments'])


@router.post('/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Create a new comment."""
    try:
        return comment_controller.create(db, obj_in=comment)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/', response_model=list[CommentResponse])
def get_comments(
    skip: int = 0,
    limit: int = 100,
    post_id: int | None = None,
    user_id: int | None = None,
    parent_id: int | None = None,
    db: Session = Depends(get_db),
):
    """Get comments with optional filtering."""
    try:
        # Build filters based on query parameters
        filters = {}
        if post_id is not None:
            filters['post_id'] = post_id
        if user_id is not None:
            filters['user_id'] = user_id
        if parent_id is not None:
            filters['parent_id'] = parent_id
        elif parent_id is None and not post_id and not user_id:
            # By default, return only top-level comments
            filters['parent_id'] = None

        return comment_controller.get_multi(db, skip=skip, limit=limit, filters=filters)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/{comment_id}', response_model=CommentDetailResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Get a specific comment by ID with author and replies"""
    try:
        return comment_controller.get_with_author_and_replies(db, comment_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.put('/{comment_id}', response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
):
    """Update a comment."""
    try:
        comment = comment_controller.get(db, comment_id)
        return comment_controller.update(db, db_obj=comment, obj_in=comment_update)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete a comment."""
    try:
        comment_controller.delete(db, id=comment_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/post/{post_id}', response_model=list[CommentResponse])
def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all comments for a specific post."""
    try:
        return comment_controller.get_comments_by_post(db, post_id, skip, limit)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/user/{user_id}', response_model=list[CommentResponse])
def get_comments_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all comments by a specific user."""
    try:
        return comment_controller.get_comments_by_user(db, user_id, skip, limit)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/replies/{parent_id}', response_model=list[CommentResponse])
def get_replies(
    parent_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all replies to a specific comment."""
    try:
        return comment_controller.get_replies(db, parent_id, skip, limit)
    except Exception as e:
        raise to_http_exception(e)


@router.post('/{parent_id}/reply', response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_reply(
    parent_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
):
    """Create a reply to an existing comment."""
    try:
        return comment_controller.create_reply(db, parent_id, comment)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)
