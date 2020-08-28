import unittest
from mongoengine import connect, disconnect
import backend.services.task as service_task
import backend.services.auth as service_auth
from backend.models.task import Task


class TestTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')
        user = {
            'username': 'user',
            'password': 'test123',
            'slack_api': 'http://slack.com'
        }
        service_auth.register(user)

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_service_create_task(self):
        task = {
            'name': 'test',
            'message': 'hello world',
            'date_schedule': '2020-08-26T07:11:07.132000'
        }
        body, status = service_task.create_task('user', task)
        data = body['data']
        assert status == 200
        assert data['name'] == 'test'
        assert data['message'] == 'hello world'

    def test_service_create_task_no_name(self):
        task = {
            'message': 'hello world',
            'date_schedule': '2020-08-26T07:11:07.132000'
        }
        body, status = service_task.create_task('user', task)
        assert status == 400
        assert body['success'] is False

    def test_service_get_all_tasks(self):
        # TODO
        # finish after setUp and tearDown will work properly
        task = {
            'name': 'test',
            'message': 'hello world',
            'date_schedule': '2020-08-26T07:11:07.132000'
        }
        service_task.create_task('user', task)
        service_task.create_task('user', task)
        body, status = service_task.get_all_tasks('user')

        data = body['data']

        print(len(data['tasks']))

        # assert len(data['tasks']) == 2
        # assert data['tasks'][0]['name'] == 'test'

    # def test_service_edit_task(self):
    #     pass

    # def test_service_delete_task(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
