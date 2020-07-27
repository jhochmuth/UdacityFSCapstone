import unittest
from flaskr import create_app
from models import db, Question
import json


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

class CastingTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = 'postgresql://{}:{}@localhost:5432/casting'.format(DB_USER, DB_PASS)

  def tearDown(self):
    pass

  def test_true(self):
    assert True



if __name__ == "__main__":
  unittest.main()
