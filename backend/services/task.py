from backend.models.user import User, user_schema
from backend.models.task import Task, task_schema
from backend.extension import scheduler
import datetime
import requests


# TODO - to common.py
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

    # TODO - catch specific exceptions: unique
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
    url = user.slack_api
    json = {'text': f'{task.name} - {task.message}'}
    requests.post(url=url, json=json)


def edit_task(current_user, json_data):
    user = get_user(current_user)

    # TODO - finish finding specific task
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


# TODO - check this week, not 7 days back
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


# TODO - check this month, not 30 days back
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
