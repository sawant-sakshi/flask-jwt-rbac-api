from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from app.models import get_user_by_email, get_user_by_id, USERS_DB

auth_bp = Blueprint("auth", __name__)


def validate_login_payload(data):
    errors = {}
    if not data.get("email"):
        errors["email"] = "Email is required"
    if not data.get("password"):
        errors["password"] = "Password is required"
    return errors


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_login_payload(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 422

    user = get_user_by_email(data["email"])
    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"email": user["email"], "role": user["role"]}
    )

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": user["id"], "name": user["name"],
            "email": user["email"], "role": user["role"]
        }
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = {}
    for field in ["name", "email", "password"]:
        if not data.get(field):
            errors[field] = f"{field.capitalize()} is required"
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 422

    if data["email"] in USERS_DB:
        return jsonify({"error": "Email already registered"}), 409

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 422

    new_id = max(u["id"] for u in USERS_DB.values()) + 1
    new_user = {
        "id": new_id, "name": data["name"], "email": data["email"],
        "password": data["password"], "role": "user"
    }
    USERS_DB[data["email"]] = new_user

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user["id"], "name": new_user["name"],
            "email": new_user["email"], "role": new_user["role"]
        }
    }), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user["id"], "name": user["name"],
        "email": user["email"], "role": user["role"]
    }), 200
