from backend.models.user import User
from backend.extension import bcrypt
from flask_jwt_extended import create_access_token
from backend.models.user import user_schema


def login(json_data):
    username = json_data.get('username', None)
    password = json_data.get('password', None)

    if username is None or password is None:
        return {'success': False, 'message': 'Username or password missing'}, 422

    user = User.objects.filter(username=username).first()

    if not bcrypt.check_password_hash(user.password, password):
        return {'success': False, 'message': 'Username or password is invalid'}, 422

    access_token = create_access_token(identity=username)
    return {'token': access_token}, 200


def register(json_data):
    try:
        password = json_data['password']
        del json_data['password']
    except KeyError as e:
        return {'success': False, 'message': 'No password'}

    try:
        user_json = user_schema.load(json_data)
    except Exception as e:
        return {'success': False, 'message': str(e)}, 422

    try:
        user = User(**user_json, password=bcrypt.generate_password_hash(password))
        user.save()
    except Exception as e:
        return {'success': False, 'message': str(e)}, 422

    return {'success': True, 'data': user}, 200
