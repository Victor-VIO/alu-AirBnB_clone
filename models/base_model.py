#!/usr/bin/python3
"""BaseModel for AirBnB clone."""
import uuid
from datetime import datetime


class BaseModel:
    """Base class that defines common attributes/methods."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        If kwargs is not empty, set attributes from kwargs (convert datetimes).
        Otherwise create new id/created_at/updated_at and register with storage.
        """
        if kwargs:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(val))
                elif key != "__class__":
                    setattr(self, key, val)
            # If some keys were missing, ensure they exist
            if not hasattr(self, "id"):
                self.id = str(uuid.uuid4())
            if not hasattr(self, "created_at"):
                self.created_at = datetime.now()
            if not hasattr(self, "updated_at"):
                self.updated_at = self.created_at
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            # Import storage here to avoid circular import at module load time
            from models import storage
            storage.new(self)

    def __str__(self):
        """Return string representation: [<class name>] (<id>) <dict>"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at and call storage.save()."""
        self.updated_at = datetime.now()
        # Import storage here to avoid circular import on module import
        from models import storage
        storage.save()

    def to_dict(self):
        """Return a dict containing all keys/values of __dict__ with ISO date strings."""
        d = self.__dict__.copy()
        d["__class__"] = self.__class__.__name__
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        return d

