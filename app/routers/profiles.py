from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import (
    ProfileCreate,
    ProfileDetailResponse,
    ProfileResponse,
    ProfileUpdate,
)


router = APIRouter(prefix='/profiles', tags=['Profiles'])


@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Create a new profile"""
    # Check if user exists
    user = db.query(User).filter(User.id == profile.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Check if user already has a profile
    existing_profile = db.query(Profile).filter(Profile.user_id == profile.user_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already has a profile',
        )

    # Create new profile
    new_profile = Profile(
        user_id=profile.user_id,
        bio=profile.bio,
        website=profile.website,
        location=profile.location,
        avatar_url=profile.avatar_url,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.get('/', response_model=list[ProfileResponse])
def get_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all profiles with pagination"""
    profiles = db.query(Profile).offset(skip).limit(limit).all()
    return profiles


@router.get('/{profile_id}', response_model=ProfileDetailResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """Get a specific profile by ID with user details"""
    profile = db.query(Profile).options(joinedload(Profile.user)).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found',
        )
    return profile


@router.get('/users/{user_id}', response_model=ProfileDetailResponse)
def get_profile_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get a profile by user ID"""
    profile = db.query(Profile).options(joinedload(Profile.user)).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found for this user',
        )
    return profile


@router.put('/{profile_id}', response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db),
):
    """Update a profile"""
    # Get the existing profile
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found',
        )

    # Update profile fields
    profile_data = profile_update.dict(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete('/{profile_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """Delete a profile"""
    # Get the existing profile
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found',
        )

    # Delete the profile
    db.delete(db_profile)
    db.commit()
