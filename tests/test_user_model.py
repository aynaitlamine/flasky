from pickle import NONE
import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User();
        u.password = "ayoub-123"
        self.assertTrue(u.password_hash is not None);

    def test_password_is_not_getter(self):
        u = User(password = "ayoub-123");
        with self.assertRaises(AttributeError):
            u.password 

    def test_password_verification(self):
        u = User();
        u.password = "ayoub-123"
        self.assertTrue(u.verify_password("ayoub-123"))
        self.assertFalse(u.verify_password("ayoub"))