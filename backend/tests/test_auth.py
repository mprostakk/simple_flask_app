import unittest
from mongoengine import connect, disconnect
import backend.services.auth as service_auth
from backend.models.user import User


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_user(self):
        user = User(username='Test', password="123", slack_api="http://www.google.pl")
        user.save()
        user_first = User.objects().first()
        assert user_first.username == 'Test'
        assert user_first.password == '123'
        assert user_first.slack_api == 'http://www.google.pl'

    def test_login_no_password(self):
        body, status = service_auth.login({
            'username': 'user'
        })
        assert status == 422

    def test_service_register_user(self):
        user = {
            'username': 'user',
            'password': 'test123',
            'slack_api': 'http://slack.com'
        }
        body, status = service_auth.register(user)
        data = body['data']
        assert status == 200
        assert data['username'] == 'user'
        assert data['password'] != 'test123'
        assert data['slack_api'] == 'http://slack.com'

    def test_service_register_user_second_unique(self):
        user = {
            'username': 'user',
            'password': 'test123',
            'slack_api': 'http://slack.com'
        }
        body, status = service_auth.register(user)
        assert status == 400


if __name__ == "__main__":
    unittest.main()
