from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request

USERS_DB = {
    "admin@example.com": {
        "id": 1, "name": "Alice Admin", "email": "admin@example.com",
        "password": "admin123", "role": "admin"
    },
    "mod@example.com": {
        "id": 2, "name": "Bob Moderator", "email": "mod@example.com",
        "password": "mod123", "role": "moderator"
    },
    "user@example.com": {
        "id": 3, "name": "Carol User", "email": "user@example.com",
        "password": "user123", "role": "user"
    }
}

PRODUCTS_DB = [
    {"id": 1, "name": "Laptop Pro", "price": 1299.99, "stock": 50},
    {"id": 2, "name": "Wireless Mouse", "price": 29.99, "stock": 200},
    {"id": 3, "name": "USB-C Hub", "price": 49.99, "stock": 150},
]

ROLE_HIERARCHY = {"user": 1, "moderator": 2, "admin": 3}


def get_user_by_email(email):
    return USERS_DB.get(email)


def get_user_by_id(user_id):
    for user in USERS_DB.values():
        if user["id"] == user_id:
            return user
    return None


def require_role(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = get_user_by_id(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 404

            user_level = ROLE_HIERARCHY.get(user["role"], 0)
            allowed = any(
                user_level >= ROLE_HIERARCHY.get(r, 0)
                for r in required_roles
            )

            if not allowed:
                return jsonify({
                    "error": "Insufficient permissions",
                    "required": list(required_roles),
                    "your_role": user["role"]
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
