from sqlalchemy.orm import Session
from typing import Optional, Any
from ..database import Base

class BaseService:
    def __init__(self, model: Any, db: Session):
        """
        Initialize the base service.
        
        Args:
            model: SQLAlchemy model class
            db: SQLAlchemy database session
        """
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[Any]:
        """Get a single record by id."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[Any]:
        """Get all records."""
        return self.db.query(self.model).all()

    def create(self, **kwargs) -> Any:
        """Create a new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, **kwargs) -> Optional[Any]:
        """Update a record by id."""
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """Delete a record by id."""
        instance = self.get(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False