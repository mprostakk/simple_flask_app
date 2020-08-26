from flask import request, jsonify
from . import bp
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
