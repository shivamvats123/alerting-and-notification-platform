from sqlalchemy.orm import Session

class BaseService:
    """Base service class for database operations."""
    
    def __init__(self, db, model_class):
        """Initialize the service with a database session and model class."""
        self.db = db
        self.model_class = model_class

    def get(self, id):
        """Get a record by ID."""
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self):
        """Get all records."""
        return self.db.query(self.model_class).all()

    def create(self, **kwargs):
        """Create a new record."""
        instance = self.model_class(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id, **kwargs):
        """Update a record by ID."""
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id):
        """Delete a record by ID."""
        instance = self.get(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False