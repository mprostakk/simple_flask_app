from backend.models.user import User
from backend.extension import bcrypt
from flask_jwt_extended import create_access_token


def login(json_data):

    # TODO - get user to common.py

    username = json_data.get('username', None)
    password = json_data.get('password', None)

    if username is None or password is None:
        return {'success': False, 'message': 'Username or password missing'}, 200

    if not username:
        return {'success': False, 'message': 'Missing username parameter'}, 400
    if not password:
        return {'success': False, 'message': 'Missing password parameter'}, 400

    user = User.objects.filter(username=username).first()

    if not bcrypt.check_password_hash(user.password, password):
        return {'success': False, 'message': 'Username or password is invalid'}, 401

    access_token = create_access_token(identity=username)
    return {'token': access_token}, 200


def register(data):

    # TODO - user schema load

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
        username = data['username']
        password = bcrypt.generate_password_hash(data['password'])
        slack_api = data['slack_api']
    except Exception as e:
        return {'success': False, 'message': 'Missing username or password'}

    try:
        user = User(username=username, password=password, slack_api=slack_api)
        user.save()
    # TODO
    # - except only not unique constraint
    except Exception as e:
        return {'success': False, 'message': 'unique'}, 400

    return {'success': True, 'data': user}, 200