#!/usr/bin/python3
"""Unit tests for FileStorage class"""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.model = BaseModel()
        self.model.name = "Test Model"
        self.model.number = 89

    def tearDown(self):
        """Clean up after tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_file_path(self):
        """Test __file_path attribute"""
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")

    def test_objects_dict(self):
        """Test __objects attribute"""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_all_method(self):
        """Test all() method"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)

    def test_new_method(self):
        """Test new() method"""
        key = f"BaseModel.{self.model.id}"
        self.storage.new(self.model)
        self.assertIn(key, self.storage.all())

    def test_save_method(self):
        """Test save() method"""
        self.storage.new(self.model)
        self.storage.save()
        
        self.assertTrue(os.path.exists("file.json"))
        with open("file.json", "r") as f:
            data = json.load(f)
        
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, data)

    def test_reload_method(self):
        """Test reload() method"""
        # First save an object
        self.storage.new(self.model)
        self.storage.save()
        
        # Clear current objects and reload
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, self.storage.all())
        
        reloaded_model = self.storage.all()[key]
        self.assertEqual(self.model.id, reloaded_model.id)
        self.assertEqual(self.model.name, reloaded_model.name)

    def test_reload_nonexistent_file(self):
        """Test reload() with non-existent file"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        
        # This should not raise an error
        self.storage.reload()

    def test_save_reload_integration(self):
        """Test save and reload integration"""
        # Create and save object
        model = BaseModel()
        model.name = "Test"
        self.storage.new(model)
        self.storage.save()
        
        # Create new storage instance and reload
        new_storage = FileStorage()
        new_storage.reload()
        
        key = f"BaseModel.{model.id}"
        self.assertIn(key, new_storage.all())
        
        reloaded = new_storage.all()[key]
        self.assertEqual(model.id, reloaded.id)
        self.assertEqual(model.name, reloaded.name)


if __name__ == '__main__':
    unittest.main()
