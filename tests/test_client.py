import unittest
import re
from app import create_app, db
from app.models import Role, User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):

        # register new account
        response = self.client.post("/auth/register", data={
            'email': 'ay@ex.com',
            'username': 'ayoub',
            'password': 'ayoub2022',
            'password_confirm': 'ayoub2022'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'A confirmation email has been sent to you by email' in response.get_data(as_text=True))

        # login with new account
        
        response = self.client.post('/auth/login', data={
            'email': 'ay@ex.com',
            'password': 'ayoub2022'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('Hello,\s+ayoub!',
                        response.get_data(as_text=True)))
        self.assertTrue(
            'You have not confirmed your account yet' in response.get_data(
                as_text=True))

        user = User.query.filter_by(email="ay@ex.com").first()
        token = user.generate_confirmation_token()

        # confirm new account

        response = self.client.get(
            f'/auth/confirm/{token}', follow_redirects=True)

        self.assertTrue(user.confirm(token))

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            'You have confirmed your account. Thanks!' in response.get_data(as_text=True))


        # logout 

        response = self.client.get("/auth/logout",  follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out.' in response.get_data(as_text=True))
