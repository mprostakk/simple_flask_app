from backend.models.user import User, user_schema
from backend.models.task import Task, task_schema
from backend.extension import scheduler
import datetime
import requests

def get_user(username):
    return User.objects.filter(username=username).first()


def get_all_tasks(current_user):
    user = get_user(current_user)
    return {"success": True, "data": user_schema.dump(user)}, 200


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
        return {"success": False, "message": str(e)}

    scheduler.add_job(
        add_task_to_schedular,
        'date',
        run_date=task.date_schedule,
        args=[user, task]
    )

    return {"success": True, "data": task_return_json}, 200


def add_task_to_schedular(user, task):

    URL = user.slack_api
    JSON = {'text': f'{task.name} - {task.message}'}
    requests.post(url=URL, json=JSON)


def edit_task(current_user, json_data):
    user = get_user(current_user)

    for task in user.tasks:
        # return {'task': task}, 200

        if task == json_data['id']:
            return {'data': task}, 200
    else:
        return {'success': False}, 400

    # try:
    #     task = Task.objects.filter(id=json_data['id'])
    # except Exception as e:
    #     return {'success': False, 'message': str(e)}, 422

    return {'success': True, 'data': 123}, 200


def delete_task(current_user, json_data):
    raise NotImplemented


def week_tasks(current_user):
    user = get_user(current_user)
    tasks = []
    for task in user.tasks:
        t = task.date_schedule
        today = datetime.datetime.now()
        timedelta = today-t
        if 0 <= timedelta.days <= 7:
            tasks.append(task)

    return {'data': tasks}, 200


def month_tasks(current_user):
    user = get_user(current_user)
    tasks = []
    for task in user.tasks:
        t = task.date_schedule
        today = datetime.datetime.now()
        timedelta = today-t
        if 0 <= timedelta.days <= 30:
            tasks.append(task)

    return {'data': tasks}, 200
