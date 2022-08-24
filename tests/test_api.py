import json
import unittest
from base64 import b64encode
from app import create_app, db
from app.models import Post, Role, User, Comment


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, email, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url', headers=self.get_api_headers('email', 'password'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)
        data = response.get_json()

        self.assertEqual(data['error'], 'not found')

    def test_bad_auth(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u = User(username="ayoub", email='ay@ex.com',
                 password="ayoub2022", confirmed=True, role=r)

        db.session.add(u)
        db.session.commit()

        response = self.client.get(
            '/api/v1/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub202'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.is_json)
        data = response.get_json()

        self.assertEqual(data['error'], 'unauthorized')

    def test_auth_token(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u = User(username="ayoub", email='ay@ex.com',
                 password="ayoub2022", confirmed=True, role=r)

        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            '/api/v1/tokens/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'))

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.is_json)

        data = response.get_json()
        token = data['token']

        response = self.client.get(
            '/api/v1/posts/', headers=self.get_api_headers(token, ''))

        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get(
            '/api/v1/posts/')

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertEqual(data['error'], 'unauthorized')

    def test_unconfirm_user(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u = User(username="ayoub", email='ay@ex.com',
                 password="ayoub2022", role=r)

        db.session.add(u)
        db.session.commit()

        response = self.client.get(
            '/api/v1/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertEqual(data['error'], 'forbidden')

    def test_posts(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u = User(username="ayoub", email='ay@ex.com',
                 password="ayoub2022", confirmed=True, role=r)

        db.session.add(u)
        db.session.commit()

        # bad body

        response = self.client.post(
            '/api/v1/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'), data=json.dumps({'body': ''}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertEqual(data['error'], 'bad request')

        # add post

        response = self.client.post(
            '/api/v1/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'), data=json.dumps({'body': 'body of the *blog* post'}))

        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')

        self.assertIsNotNone(url)

        # single post

        response = self.client.get(
            url, headers=self.get_api_headers('ay@ex.com', 'ayoub2022'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data['body'], 'body of the *blog* post')

        # post update
        response = self.client.put(
            url, headers=self.get_api_headers('ay@ex.com', 'ayoub2022'), data=json.dumps({'body': 'update body post'}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data['body'], 'update body post')

    def test_users(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u1 = User(username="ayoub", email='ay@ex.com',
                  password="ayoub2022", confirmed=True, role=r)

        u2 = User(username="morad", email='ma@ex.com',
                  password="morad2022", confirmed=True, role=r)

        db.session.add_all([u1, u2])
        db.session.commit()

        # add post

        response = self.client.post(
            '/api/v1/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'), data=json.dumps({'body': 'body of the *blog* post'}))

        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')

        self.assertIsNotNone(url)

        # user posts

        response = self.client.get(
            f'/api/v1/users/{u1.id}/posts/', headers=self.get_api_headers('ay@ex.com', 'ayoub2022'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(len(data['posts']), 1)

        u2.follow(u1)

        db.session.add(u2)
        db.session.commit()

        self.assertTrue(u2.is_following(u1))

        response = self.client.get(
            f'/api/v1/users/{u2.id}/timeline/', headers=self.get_api_headers('ma@ex.com', 'morad2022'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(len(data['posts']), 1)

    def test_comments(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)
        u1 = User(username="ayoub", email='ay@ex.com',
                  password="ayoub2022", confirmed=True, role=r)

        u2 = User(username="morad", email='ma@ex.com',
                  password="morad2022", confirmed=True, role=r)

        db.session.add_all([u1, u2])
        db.session.commit()

        # add post
        post = Post(body='Blog post body', author=u1)
        db.session.add(post)
        db.session.commit()

        # get all comments

        response = self.client.get(
            f'/api/v1/posts/{post.id}/comments/', headers=self.get_api_headers('ma@ex.com', 'morad2022'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()

        self.assertEqual(len(data['comments']), 0)

        # add two comment

        c1 = Comment(body='Good job', author=u2, post=post)
        c2 = Comment(body='Thank you!', author=u1, post=post)
        db.session.add_all([c1, c2])
        db.session.commit()

        response = self.client.get(
            f'/api/v1/posts/{post.id}/comments/', headers=self.get_api_headers('ma@ex.com', 'morad2022'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()

        self.assertEqual(len(data['comments']), 2)
