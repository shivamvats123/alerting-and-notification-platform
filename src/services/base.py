from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Optional, Dict, List, Any, Union

class BaseService:
    """
    Base service class for database operations.
    """
    def __init__(self, db: Session, model_class: DeclarativeMeta) -> None:
        self.db = db
        self.model_class = model_class

    def get(self, id: int) -> Optional[DeclarativeMeta]:
        """
        Get a record by ID.
        """
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self) -> List[DeclarativeMeta]:
        """
        Get all records.
        """
        return self.db.query(self.model_class).all()

    def create(self, data: Dict[str, Any]) -> DeclarativeMeta:
        """
        Create a new record.
        """
        instance = self.model_class(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, data: Dict[str, Any]) -> Optional[DeclarativeMeta]:
        """
        Update a record by ID.
        """
        instance = self.get(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        """
        instance = self.get(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False