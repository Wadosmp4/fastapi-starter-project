from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.controllers.base import BaseCRUDController
from app.exceptions import ConflictException, NotFoundException
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileDetailResponse, ProfileUpdate


class ProfileController(BaseCRUDController[Profile, ProfileCreate, ProfileUpdate]):
    """
    Profile-specific CRUD controller with additional profile-related operations.
    """

    def __init__(self):
        super().__init__(Profile)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[Profile]:
        """
        Get profile by user ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Profile instance or None if not found
        """
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    def create(self, db: Session, *, obj_in: ProfileCreate) -> Profile:
        """
        Create a new profile with validation for unique user_id.

        Args:
            db: Database session
            obj_in: Profile creation data

        Returns:
            Created profile instance

        Raises:
            ConflictException: If profile for user already exists
        """
        # Check if profile for user already exists
        if self.get_by_user_id(db, obj_in.user_id):
            raise ConflictException(f'Profile for user {obj_in.user_id} already exists')

        return super().create(db, obj_in=obj_in)

    def get_with_user(self, db: Session, profile_id: int) -> ProfileDetailResponse:
        """
        Get a profile with its user loaded.

        Args:
            db: Database session
            profile_id: Profile ID

        Returns:
            ProfileDetailResponse with user

        Raises:
            NotFoundException: If profile not found
        """
        profile = db.query(Profile).options(joinedload(Profile.user)).filter(Profile.id == profile_id).first()

        if not profile:
            raise NotFoundException(f'Profile with id {profile_id} not found')

        return ProfileDetailResponse.from_orm(profile)

    def get_by_username(self, db: Session, username: str) -> Optional[ProfileDetailResponse]:
        """
        Get profile by username.

        Args:
            db: Database session
            username: Username

        Returns:
            ProfileDetailResponse with user or None if not found
        """
        profile = (
            db.query(Profile).options(joinedload(Profile.user)).filter(Profile.user.has(username=username)).first()
        )

        if not profile:
            return None

        return ProfileDetailResponse.from_orm(profile)

    def update_by_user_id(self, db: Session, user_id: int, obj_in: ProfileUpdate) -> Profile:
        """
        Update profile by user ID.

        Args:
            db: Database session
            user_id: User ID
            obj_in: Profile update data

        Returns:
            Updated profile instance

        Raises:
            NotFoundException: If profile not found
        """
        profile = self.get_by_user_id(db, user_id)
        if not profile:
            raise NotFoundException(f'Profile for user {user_id} not found')

        return self.update(db, db_obj=profile, obj_in=obj_in)

    def get_profiles_by_location(self, db: Session, location: str, skip: int = 0, limit: int = 100) -> list[Profile]:
        """
        Get profiles by location.

        Args:
            db: Database session
            location: Location to search for
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of profiles in the location
        """
        return self.get_multi(db, skip=skip, limit=limit, filters={'location': location})


# Create a singleton instance
profile_controller = ProfileController()
