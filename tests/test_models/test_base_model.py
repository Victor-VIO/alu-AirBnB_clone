import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    def test_instance(self):
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)

if __name__ == "__main__":
    unittest.main()

