from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.post import Post, PostCategory
from app.models.user import User
from app.schemas.post import PostCreate, PostDetailResponse, PostResponse, PostUpdate


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post('/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new post"""
    # Check if user exists
    user = db.query(User).filter(User.id == post.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Create new post
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/', response_model=list[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    """Get all posts with optional filtering"""
    query = db.query(Post)

    if user_id:
        query = query.filter(Post.user_id == user_id)

    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts


@router.get('/{post_id}', response_model=PostDetailResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID with author details"""
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    # Format the response with author details
    result = PostDetailResponse.from_orm(post)
    result.author = {
        'id': post.author.id,
        'username': post.author.username,
    }

    return result


@router.put('/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    """Update a post"""
    # Get the existing post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    # Update post fields
    post_data = post_update.dict(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    # Get the existing post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    # Delete the post
    db.delete(db_post)
    db.commit()


@router.post('/{post_id}/categories/{category_id}', response_model=PostResponse)
def add_category_to_post(post_id: int, category_id: int, db: Session = Depends(get_db)):
    """Add a category to a post"""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    # Check if category exists
    from app.models.category import Category

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found',
        )

    # Check if the relationship already exists
    existing = (
        db.query(PostCategory)
        .filter(
            PostCategory.post_id == post_id,
            PostCategory.category_id == category_id,
        )
        .first()
    )

    if not existing:
        # Create the association
        post_category = PostCategory(post_id=post_id, category_id=category_id)
        db.add(post_category)
        db.commit()

    return post


@router.delete('/{post_id}/categories/{category_id}', response_model=PostResponse)
def remove_category_from_post(
    post_id: int,
    category_id: int,
    db: Session = Depends(get_db),
):
    """Remove a category from a post"""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    # Check if the relationship exists
    existing = (
        db.query(PostCategory)
        .filter(
            PostCategory.post_id == post_id,
            PostCategory.category_id == category_id,
        )
        .first()
    )

    if existing:
        # Delete the association
        db.delete(existing)
        db.commit()

    return post
