#!/usr/bin/python3
import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    def test_id_type(self):
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)

    def test_save_updates_time(self):
        obj = BaseModel()
        old = obj.updated_at
        obj.save()
        self.assertNotEqual(old, obj.updated_at)

if __name__ == "__main__":
    unittest.main()

