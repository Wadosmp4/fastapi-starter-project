from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.controllers.base import BaseCRUDController
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password


class UserController(BaseCRUDController[User, UserCreate, UserUpdate]):
    """
    User-specific CRUD controller with additional user-related operations.
    """

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: User's email address

        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: User's username

        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user with validation for unique email and username.

        Args:
            db: Database session
            obj_in: User creation data

        Returns:
            Created user instance

        Raises:
            ConflictException: If email or username already exists
        """
        # Hash the password
        hashed_password = hash_password(obj_in.password)
        user_data = obj_in.dict(exclude={'password'})
        user_data['hashed_password'] = hashed_password
        db_obj = User(**user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Get all active users.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        return self.get_multi(db, skip=skip, limit=limit, filters={'is_active': True}, order_by=desc(User.created_at))

    def deactivate_user(self, db: Session, user_id: int) -> User:
        """
        Deactivate a user (soft delete).

        Args:
            db: Database session
            user_id: User ID to deactivate

        Returns:
            Updated user instance
        """
        user = self.get(db, user_id)
        return self.update(db, db_obj=user, obj_in={'is_active': False})

    def activate_user(self, db: Session, user_id: int) -> User:
        """
        Activate a user.

        Args:
            db: Database session
            user_id: User ID to activate

        Returns:
            Updated user instance
        """
        user = self.get(db, user_id)
        return self.update(db, db_obj=user, obj_in={'is_active': True})


# Create a singleton instance
user_controller = UserController()
