from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.database import get_db
from app.exceptions import ConflictException, NotFoundException, to_http_exception
from app.schemas.user import UserCreate, UserResponse, UserUpdate


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    try:
        return user_controller.create(db, obj_in=user)
    except ConflictException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/', response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users."""
    try:
        return user_controller.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/active', response_model=list[UserResponse])
def get_active_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all active users."""
    try:
        return user_controller.get_active_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    try:
        return user_controller.get(db, id=user_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update a user."""
    try:
        user = user_controller.get(db, id=user_id)
        return user_controller.update(db, db_obj=user, obj_in=user_update)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user."""
    try:
        user_controller.delete(db, id=user_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.post('/{user_id}/deactivate', response_model=UserResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Deactivate a user."""
    try:
        return user_controller.deactivate_user(db, user_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.post('/{user_id}/activate', response_model=UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """Activate a user."""
    try:
        return user_controller.activate_user(db, user_id)
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/email/{email}', response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get a user by email address."""
    try:
        user = user_controller.get_by_email(db, email)
        if not user:
            raise NotFoundException(f'User with email {email} not found')
        return user
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)


@router.get('/username/{username}', response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get a user by username."""
    try:
        user = user_controller.get_by_username(db, username)
        if not user:
            raise NotFoundException(f'User with username {username} not found')
        return user
    except NotFoundException as e:
        raise to_http_exception(e)
    except Exception as e:
        raise to_http_exception(e)
