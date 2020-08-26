import unittest
from mongoengine import connect, disconnect
import backend.services.task as service_task
import backend.services.auth as service_auth
from backend.models.task import Task
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

    def test_service_create_user(self):

        service_auth.register()
        service_auth.login()


if __name__ == "__main__":
    unittest.main()