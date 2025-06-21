from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.controllers.base import BaseCRUDController
from app.exceptions import ConflictException, DatabaseException, NotFoundException
from app.models.role import Role, UserRole
from app.models.user import User
from app.schemas.role import RoleCreate, RoleDetailResponse, RoleUpdate


class RoleController(BaseCRUDController[Role, RoleCreate, RoleUpdate]):
    """
    Role-specific CRUD controller with additional role-related operations.
    """

    def __init__(self):
        super().__init__(Role)

    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        """
        Get role by name.

        Args:
            db: Database session
            name: Role name

        Returns:
            Role instance or None if not found
        """
        return db.query(Role).filter(Role.name == name).first()

    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        """
        Create a new role with validation for unique name.

        Args:
            db: Database session
            obj_in: Role creation data

        Returns:
            Created role instance

        Raises:
            ConflictException: If role name already exists
        """
        # Check if role name already exists
        if self.get_by_name(db, obj_in.name):
            raise ConflictException(f"Role with name '{obj_in.name}' already exists")

        return super().create(db, obj_in=obj_in)

    def get_with_users(self, db: Session, role_id: int) -> RoleDetailResponse:
        """
        Get a role with its users loaded.

        Args:
            db: Database session
            role_id: Role ID

        Returns:
            RoleDetailResponse with users

        Raises:
            NotFoundException: If role not found
        """
        role = db.query(Role).options(joinedload(Role.users)).filter(Role.id == role_id).first()

        if not role:
            raise NotFoundException(f'Role with id {role_id} not found')

        return RoleDetailResponse.from_orm(role)

    def assign_role_to_user(self, db: Session, user_id: int, role_id: int) -> UserRole:
        """
        Assign a role to a user.

        Args:
            db: Database session
            user_id: User ID
            role_id: Role ID

        Returns:
            UserRole instance

        Raises:
            ConflictException: If role is already assigned to user
            NotFoundException: If user or role not found
        """
        # Check if role is already assigned to user
        existing_assignment = (
            db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()
        )

        if existing_assignment:
            raise ConflictException(f'Role {role_id} is already assigned to user {user_id}')

        # Create new assignment
        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.add(user_role)
        db.commit()
        db.refresh(user_role)

        return user_role

    def remove_role_from_user(self, db: Session, user_id: int, role_id: int) -> bool:
        """
        Remove a role from a user.

        Args:
            db: Database session
            user_id: User ID
            role_id: Role ID

        Returns:
            True if role was removed, False if not found

        Raises:
            DatabaseException: If removal fails
        """
        try:
            user_role = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()

            if not user_role:
                return False

            db.delete(user_role)
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            raise DatabaseException(f'Failed to remove role {role_id} from user {user_id}: {str(e)}')

    def get_user_roles(self, db: Session, user_id: int) -> List[Role]:
        """
        Get all roles assigned to a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of roles assigned to the user
        """
        return db.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()

    def get_users_with_role(self, db: Session, role_id: int) -> List[User]:
        """
        Get all users with a specific role.

        Args:
            db: Database session
            role_id: Role ID

        Returns:
            List of users with the role
        """
        return db.query(User).join(UserRole).filter(UserRole.role_id == role_id).all()


# Create a singleton instance
role_controller = RoleController()
