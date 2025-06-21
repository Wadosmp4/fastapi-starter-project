from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.exceptions import DatabaseException, NotFoundException


ModelType = TypeVar('ModelType', bound=Any)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUDController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD controller with common database operations.

    Generic types:
    - ModelType: SQLAlchemy model class
    - CreateSchemaType: Pydantic model for creation
    - UpdateSchemaType: Pydantic model for updates
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize the controller with a model.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType:
        """
        Get a single record by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            Model instance

        Raises:
            NotFoundException: If record not found
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise NotFoundException(f'{self.model.__name__} with id {id} not found')
        return obj

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
        order_by: Optional[Any] = None,
    ) -> List[ModelType]:
        """
        Get multiple records with optional filtering and pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of field-value pairs to filter by
            order_by: SQLAlchemy order_by clause

        Returns:
            List of model instances
        """
        query = db.query(self.model)

        # Apply filters
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if value is None:
                        filter_conditions.append(getattr(self.model, field).is_(None))
                    else:
                        filter_conditions.append(getattr(self.model, field) == value)

            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        # Apply ordering
        if order_by:
            query = query.order_by(order_by)

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db: Database session
            obj_in: Pydantic model with creation data

        Returns:
            Created model instance

        Raises:
            DatabaseException: If creation fails
        """
        try:
            obj_data = obj_in.dict()
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseException(f'Failed to create {self.model.__name__}: {str(e)}')

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        """
        Update an existing record.

        Args:
            db: Database session
            db_obj: Existing model instance
            obj_in: Pydantic model or dict with update data

        Returns:
            Updated model instance

        Raises:
            DatabaseException: If update fails
        """
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseException(f'Failed to update {self.model.__name__}: {str(e)}')

    def delete(self, db: Session, *, id: Any) -> ModelType:
        """
        Delete a record by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            Deleted model instance

        Raises:
            NotFoundException: If record not found
            DatabaseException: If deletion fails
        """
        try:
            obj = self.get(db, id)
            db.delete(obj)
            db.commit()
            return obj
        except NotFoundException:
            raise
        except Exception as e:
            db.rollback()
            raise DatabaseException(f'Failed to delete {self.model.__name__}: {str(e)}')

    def exists(self, db: Session, id: Any) -> bool:
        """
        Check if a record exists by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            True if record exists, False otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def count(self, db: Session, *, filters: Optional[dict] = None) -> int:
        """
        Count records with optional filtering.

        Args:
            db: Database session
            filters: Dictionary of field-value pairs to filter by

        Returns:
            Number of records
        """
        query = db.query(self.model)

        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if value is None:
                        filter_conditions.append(getattr(self.model, field).is_(None))
                    else:
                        filter_conditions.append(getattr(self.model, field) == value)

            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        return query.count()
