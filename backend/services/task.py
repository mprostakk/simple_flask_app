from backend.models.user import User, user_schema
from backend.models.task import Task, task_schema, tasks_schema
from backend.extension import scheduler
import datetime
import requests


def get_user(username):
    return User.objects.filter(username=username).first()


def get_all_tasks(current_user):
    user = get_user(current_user)
    return {'success': True, 'data': user_schema.dump(user)}, 200


def create_task(current_user, json_data):
    # 2020-08-26T07:11:07.132000
    try:
        task_json = task_schema.load(json_data)
        task = Task(**task_json)
        user = get_user(current_user)
        user.tasks.append(task)
        user.save()
        task_return_json = task_schema.dump(task)
    except Exception as e:
        return {'success': False, 'message': 'Error while saving task to user'}, 422

    scheduler.add_job(
        add_task_to_scheduler,
        'date',
        run_date=task.date_schedule,
        args=[user, task]
    )

    return {'success': True, 'data': task_return_json}, 200


def add_task_to_scheduler(user, task):
    url = user.slack_api
    json = {'text': f'{task.name} - {task.message}'}
    requests.post(url=url, json=json)


def edit_task(current_user, json_data):
    user = get_user(current_user)
    try:
        id_task = json_data['id']
    except KeyError as e:
        return {'success': False, 'message': 'Not id field'}, 422

    try:
        data = json_data['data']
    except KeyError as e:
        return {'success': False, 'message': 'No data object'}, 422

    for count, task in enumerate(user.tasks):
        if str(task._id) == id_task:
            task_json = task_schema.load(data)

            for key, value in task_json.items():
                setattr(task, key, value)

            user.save()
            return {'success': True, 'data': task_schema.dump(task)}, 200

    return {'success': False, 'message': 'Task not found'}, 400


def delete_task(current_user, json_data):
    user = get_user(current_user)
    id_task = json_data['id']

    for count, task in enumerate(user.tasks):
        if str(task._id) == id_task:
            user.tasks.pop(count)
            user.save()
            return {'success': True, 'data': user_schema.dump(user)}, 200

    return {'success': False, 'message': 'Not found'}, 400


def week_tasks(current_user):
    user = get_user(current_user)
    tasks = []
    for task in user.tasks:
        t = task.date_schedule
        today = datetime.datetime.now()
        timedelta = today-t
        if 0 <= timedelta.days <= 7:
            tasks.append(task)

    return {'data': tasks_schema.dump(tasks)}, 200


def month_tasks(current_user):
    user = get_user(current_user)
    tasks = []
    for task in user.tasks:
        t = task.date_schedule
        today = datetime.datetime.now()
        timedelta = today-t
        if 0 <= timedelta.days <= 30:
            tasks.append(task)

    return {'data': tasks_schema.dump(tasks)}, 200
