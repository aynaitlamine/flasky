from pickle import NONE
import unittest
from app import db
from app.models import AnonymousUser, Permission, User, Role


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        Role.insert_roles()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

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

    def test_user_role(self):
        u = User(email='ay@example.com', password="ayoub-123")
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))