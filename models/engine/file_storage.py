#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
import shlex
from models.base_model import BaseModel


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances.
    """
    def __init__(self):
        """Initialize the FileStorage class."""
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        """Return a dictionary of objects, filtered by class if specified."""
        result = {}
        for key, obj in self.__objects.items():
            if cls is None or obj.__class__ == cls:
                result[key] = obj
        return result

    def new(self, obj):
        """Add a new object to the __objects dictionary."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize the __objects dictionary to a JSON file."""
        my_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """Deserialize the JSON file and populate the __objects dictionary."""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                my_dict = json.load(f)
                for key, obj_dict in my_dict.items():
                    obj = eval(obj_dict["__class__"])(**obj_dict)
                    self.__objects[key] = obj
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Delete an object from __objects."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Reload the __objects dictionary."""
        self.reload()
