#!/usr/bin/python3
"""File storage engine for AirBnB clone project."""
import json
import os

# Import model classes (no storage import here to avoid circular import)
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Review": Review
}


class FileStorage:
    """Serializes instances to JSON file and deserializes back."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return self.__class__.__objects

    def new(self, obj):
        """Add obj to __objects with key <class name>.id"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__class__.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file."""
        obj_dict = {}
        for key, obj in self.__class__.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__class__.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize the JSON file to __objects, if the file exists."""
        if not os.path.exists(self.__class__.__file_path):
            return
        try:
            with open(self.__class__.__file_path, "r", encoding="utf-8") as f:
                objs = json.load(f)
            for key, val in objs.items():
                cls_name = val.get("__class__")
                if cls_name in classes:
                    # create instance using the class constructor with kwargs
                    self.__class__.__objects[key] = classes[cls_name](**val)
        except Exception:
            # if anything goes wrong (corrupt file), don't raise; leave __objects empty
            pass

