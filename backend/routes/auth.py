from flask import request, jsonify
from . import bp
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from backend.extension import db, bcrypt
from backend.models.user import User


@bp.route('/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.objects.filter(username=username).first()

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Username or password is invalid'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@bp.route('/auth/register', methods=['POST'])
def register():

    data = request.json

    # TODO (look above)
    # - serialize better
    # - error handling

    username = data['username']
    password = bcrypt.generate_password_hash(data['password'])

    user = User(username=username, password=password)
    try:
        user.save()
    # TODO
    # - except only not unique constraint
    except Exception as e:
        return jsonify({'success': False, 'message': 'unique'}), 400

    return jsonify({'success': True, 'data': user}), 200


@bp.route('/auth/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity

    current_user = get_jwt_identity()

    return jsonify(logged_in_as=current_user), 200