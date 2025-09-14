#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
import os
import json
from datetime import datetime
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        self.model = BaseModel()
        self.model2 = BaseModel()

    def tearDown(self):
        """Clean up after tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_instance_creation(self):
        """Test that instance is created properly"""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model2, BaseModel)

    def test_id_generation(self):
        """Test that each instance has unique ID"""
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model2.id, str)
        self.assertNotEqual(self.model.id, self.model2.id)
        self.assertTrue(len(self.model.id) == 36)  # UUID length

    def test_created_at_type(self):
        """Test that created_at is datetime object"""
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model2.created_at, datetime)

    def test_updated_at_type(self):
        """Test that updated_at is datetime object"""
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertIsInstance(self.model2.updated_at, datetime)

    def test_str_representation(self):
        """Test __str__ method"""
        expected = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected)

    def test_save_method(self):
        """Test save method updates updated_at"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)
        self.assertGreater(self.model.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """Test to_dict method returns correct dictionary"""
        obj_dict = self.model.to_dict()
        
        self.assertIsInstance(obj_dict, dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertEqual(obj_dict['id'], self.model.id)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertIsInstance(obj_dict['created_at'], str)
        self.assertIsInstance(obj_dict['updated_at'], str)

    def test_to_dict_datetime_format(self):
        """Test datetime format in to_dict"""
        obj_dict = self.model.to_dict()
        # Check ISO format
        try:
            datetime.fromisoformat(obj_dict['created_at'])
            datetime.fromisoformat(obj_dict['updated_at'])
        except ValueError:
            self.fail("Datetime not in ISO format")

    def test_recreate_from_dict(self):
        """Test recreating instance from dictionary"""
        original_dict = self.model.to_dict()
        new_model = BaseModel(**original_dict)
        
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)
        self.assertEqual(self.model.__dict__, new_model.__dict__)

    def test_save_reload(self):
        """Test saving and reloading from storage"""
        model = BaseModel()
        model.name = "Test Model"
        model.save()
        
        # Clear current storage and reload
        storage.reload()
        all_objs = storage.all()
        key = f"BaseModel.{model.id}"
        
        self.assertIn(key, all_objs)
        reloaded_model = all_objs[key]
        self.assertEqual(model.id, reloaded_model.id)
        self.assertEqual(model.name, reloaded_model.name)

    def test_attribute_assignment(self):
        """Test assigning attributes to BaseModel"""
        self.model.name = "Test"
        self.model.number = 89
        self.assertEqual(self.model.name, "Test")
        self.assertEqual(self.model.number, 89)

    def test_kwargs_initialization(self):
        """Test initialization with kwargs"""
        test_dict = {
            'id': 'test-id',
            'created_at': '2023-01-01T12:00:00.000000',
            'updated_at': '2023-01-01T12:00:00.000000',
            'name': 'Test',
            'number': 89,
            '__class__': 'BaseModel'
        }
        
        model = BaseModel(**test_dict)
        self.assertEqual(model.id, 'test-id')
        self.assertEqual(model.name, 'Test')
        self.assertEqual(model.number, 89)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)


if __name__ == '__main__':
    unittest.main()
