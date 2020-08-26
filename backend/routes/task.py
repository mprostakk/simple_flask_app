from flask import request, jsonify
from . import bp
import backend.services.task as task_service
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@bp.route('/task', methods=['GET'])
@jwt_required
def tasks_all():
    current_user = get_jwt_identity()
    body, status = task_service.get_all_tasks(current_user)
    return jsonify(body), status


@bp.route('/task', methods=['POST'])
@jwt_required
def task_create():
    current_user = get_jwt_identity()
    json_data = request.json
    body, status = task_service.create_task(current_user, json_data)
    return jsonify(body), status


@bp.route('/task', methods=['PATCH'])
@jwt_required
def task_edit():
    current_user = get_jwt_identity()
    json_data = request.json
    body, status = task_service.edit_task(current_user, json_data)
    return jsonify(body), status


@bp.route('/task', methods=['DELETE'])
@jwt_required
def task_delete():
    current_user = get_jwt_identity()
    json_data = request.json
    body, status = task_service.delete_task(current_user, json_data)
    return jsonify(body), status


# TODO
# - week, month as filters
@bp.route('/task/week', methods=['GET'])
@jwt_required
def get_tasks_week():
    current_user = get_jwt_identity()
    body, status = task_service.week_tasks(current_user)
    return jsonify(body), status


@bp.route('/task/month', methods=['GET'])
@jwt_required
def get_tasks_month():
    current_user = get_jwt_identity()
    body, status = task_service.month_tasks(current_user)
    return jsonify(body), status
