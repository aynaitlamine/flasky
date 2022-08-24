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
        u = User()
        u.password = "ayoub-123"
        self.assertTrue(u.password_hash is not None)

    def test_password_is_not_getter(self):
        u = User(password="ayoub-123")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User()
        u.password = "ayoub-123"
        self.assertTrue(u.verify_password("ayoub-123"))
        self.assertFalse(u.verify_password("ayoub"))

    def test_user_confirmation(self):
        u = User(email='ay@example.com', password="ayoub-123")
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_user_invalid_confirmation(self):
        u1 = User(email='ay@example.com', password="ayoub-123")
        u2 = User(email='mo@example.com', password="morad-123")
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

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

    def test_moderator_role(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='ay@example.com', password="ayoub-123", role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='ay@example.com', password="ayoub-123", role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))

    def test_follows(self):
        u1 = User(email='ay@example.com', password="ayoub-123")
        u2 = User(email='mo@example.com', password="morad-123")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))

    def test_unfollows(self):
        u1 = User(email='ay@example.com', password="ayoub-123")
        u2 = User(email='mo@example.com', password="morad-123")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()

        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))
