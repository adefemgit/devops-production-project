from flask import Blueprint, jsonify, request
from app import db
from app.models import Task

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "task-api"
    }), 200


@bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict()), 200


@bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    task = Task(
        title=data["title"],
        completed=data.get("completed", False)
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        task.title = data["title"]

    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()

    return jsonify(task.to_dict()), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"}), 200