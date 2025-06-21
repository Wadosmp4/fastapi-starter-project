from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryDetailResponse,
    CategoryResponse,
    CategoryUpdate,
)


router = APIRouter(prefix='/categories', tags=['Categories'])


@router.post('/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    # Check if category with same name already exists
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Category with this name already exists',
        )

    # Create new category
    new_category = Category(
        name=category.name,
        description=category.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get('/', response_model=list[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories with pagination"""
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.get('/{category_id}', response_model=CategoryDetailResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID with associated posts."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found',
        )
    return category


@router.put('/{category_id}', response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
):
    """Update a category."""
    # Get the existing category
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found',
        )

    # Check name uniqueness if name is being updated
    if category_update.name and category_update.name != db_category.name:
        existing = db.query(Category).filter(Category.name == category_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category with this name already exists',
            )

    # Update category fields
    category_data = category_update.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""
    # Get the existing category
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found',
        )

    # Delete the category
    db.delete(db_category)
    db.commit()
