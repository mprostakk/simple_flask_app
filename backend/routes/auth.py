from flask import request, jsonify
from . import bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
import backend.services.auth as auth_service


@bp.route('/auth/login', methods=['POST'])
def login():
    json_data = request.json
    body, status = auth_service.login(json_data)
    return jsonify(body), status


@bp.route('/auth/register', methods=['POST'])
def register():
    json_data = request.json
    body, status = auth_service.register(json_data)
    return jsonify(body), status


@bp.route('/auth/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
