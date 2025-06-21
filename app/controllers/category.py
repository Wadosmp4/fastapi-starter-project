from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.controllers.base import BaseCRUDController
from app.exceptions import ConflictException
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryController(BaseCRUDController[Category, CategoryCreate, CategoryUpdate]):
    """
    Category-specific CRUD controller with additional category-related operations.
    """

    def __init__(self):
        super().__init__(Category)

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """
        Get category by name.

        Args:
            db: Database session
            name: Category name

        Returns:
            Category instance or None if not found
        """
        return db.query(Category).filter(Category.name == name).first()

    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        """
        Create a new category with validation for unique name.

        Args:
            db: Database session
            obj_in: Category creation data

        Returns:
            Created category instance

        Raises:
            ConflictException: If category name already exists
        """
        # Check if category name already exists
        if self.get_by_name(db, obj_in.name):
            raise ConflictException(f"Category with name '{obj_in.name}' already exists")

        return super().create(db, obj_in=obj_in)

    def get_popular_categories(self, db: Session, limit: int = 10) -> list[Category]:
        """
        Get categories ordered by number of posts (most popular first).

        Args:
            db: Database session
            limit: Maximum number of records to return

        Returns:
            List of popular categories
        """
        from sqlalchemy import func

        return (
            db.query(Category)
            .outerjoin(Category.posts)
            .group_by(Category.id)
            .order_by(desc(func.count(Category.posts)))
            .limit(limit)
            .all()
        )

    def get_categories_with_post_count(self, db: Session, skip: int = 0, limit: int = 100) -> list[dict]:
        """
        Get categories with their post counts.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of categories with post counts
        """
        from sqlalchemy import func

        result = (
            db.query(Category, func.count(Category.posts).label('post_count'))
            .outerjoin(Category.posts)
            .group_by(Category.id)
            .order_by(desc(func.count(Category.posts)))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [{'category': category, 'post_count': post_count} for category, post_count in result]


# Create a singleton instance
category_controller = CategoryController()
