from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.role import Role, UserRole
from app.models.user import User
from app.schemas.role import RoleCreate, RoleDetailResponse, RoleResponse, RoleUpdate


router = APIRouter(prefix='/roles', tags=['Roles'])


@router.post('/', response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    # Check if role with same name already exists
    existing_role = db.query(Role).filter(Role.name == role.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Role with this name already exists',
        )

    # Create new role
    new_role = Role(
        name=role.name,
        description=role.description,
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.get('/', response_model=list[RoleResponse])
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all roles with pagination"""
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.get('/{role_id}', response_model=RoleDetailResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID with associated users"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )
    return role


@router.put('/{role_id}', response_model=RoleResponse)
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    """Update a role"""
    # Get the existing role
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )

    # Check name uniqueness if name is being updated
    if role_update.name and role_update.name != db_role.name:
        existing = db.query(Role).filter(Role.name == role_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Role with this name already exists',
            )

    # Update role fields
    role_data = role_update.dict(exclude_unset=True)
    for key, value in role_data.items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role


@router.delete('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role"""
    # Get the existing role
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )

    # Delete the role
    db.delete(db_role)
    db.commit()


@router.post('/{role_id}/users/{user_id}', response_model=RoleResponse)
def assign_role_to_user(role_id: int, user_id: int, db: Session = Depends(get_db)):
    """Assign a role to a user"""
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Check if the relationship already exists
    existing = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()

    if not existing:
        # Create the association
        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.add(user_role)
        db.commit()

    return role


@router.delete('/{role_id}/users/{user_id}', response_model=RoleResponse)
def remove_role_from_user(role_id: int, user_id: int, db: Session = Depends(get_db)):
    """Remove a role from a user"""
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )

    # Check if the relationship exists
    existing = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()

    if existing:
        # Delete the association
        db.delete(existing)
        db.commit()

    return role
