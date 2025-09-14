#!/usr/bin/python3
"""FileStorage class definition"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to JSON file and deserializes back to instances"""
    
    __file_path = "file.json"
    __objects = {}
    
    # Class mapping for all models
    __class_map = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }
    
    def all(self):
        """Return the dictionary __objects"""
        return FileStorage.__objects
    
    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj
    
    def save(self):
        """Serialize __objects to the JSON file"""
        obj_dict = {}
        for key, obj in FileStorage.__objects.items():
            obj_dict[key] = obj.to_dict()
        
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f)
    
    def reload(self):
        """Deserialize the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    if class_name in FileStorage.__class_map:
                        cls = FileStorage.__class_map[class_name]
                        self.new(cls(**value))
        except FileNotFoundError:
            pass
