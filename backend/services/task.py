# from backend.extension import db
# from backend.models.task import Task
from backend.models.user import User, user_schema
from backend.models.task import Task, task_schema
# import datetime


def get_user(username):
    return User.objects.filter(username=username).first()


def get_all_tasks(current_user):
    user = get_user(current_user)
    return {"success": True, "data": user_schema.dump(user)}, 200


def create_task(current_user, json_data):

    # 2020-08-26T07:11:07.132000

    # try:
    #     user_json = user_schema.load(json_data)
    # except Exception as e:
    #     raise e
    #
    # try:
    #     user = User(**user_json)
    #     user.save()
    # except Exception as e:
    #     raise e

    try:
        task_json = task_schema.load(json_data)
        task = Task(**task_json)
        user = get_user(current_user)
        user.tasks.append(task)
        user.save()

        task_return_json = task_schema.dump(task)

    except Exception as e:
        return {"success": False, "message": str(e)}

    return {"success": True, "data": task_return_json}, 200
