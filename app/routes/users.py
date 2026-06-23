from flask import Blueprint, jsonify, request
from app.models import USERS_DB, get_user_by_id, require_role

users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["GET"])
@require_role("moderator", "admin")
def list_users():
    users = [
        {"id": u["id"], "name": u["name"], "email": u["email"], "role": u["role"]}
        for u in USERS_DB.values()
    ]
    return jsonify({"users": users, "total": len(users)}), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@require_role("moderator", "admin")
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with id {user_id} not found"}), 404
    return jsonify({
        "id": user["id"], "name": user["name"],
        "email": user["email"], "role": user["role"]
    }), 200


@users_bp.route("/<int:user_id>/role", methods=["PATCH"])
@require_role("admin")
def update_role(user_id):
    data = request.get_json(silent=True)
    if not data or not data.get("role"):
        return jsonify({"error": "Field 'role' is required"}), 422

    valid_roles = ["user", "moderator", "admin"]
    if data["role"] not in valid_roles:
        return jsonify({"error": "Invalid role", "valid_roles": valid_roles}), 422

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with id {user_id} not found"}), 404

    user["role"] = data["role"]
    return jsonify({
        "message": "Role updated successfully",
        "user_id": user_id, "new_role": user["role"]
    }), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@require_role("admin")
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with id {user_id} not found"}), 404

    email = user["email"]
    del USERS_DB[email]
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200
