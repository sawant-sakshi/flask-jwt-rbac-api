from flask import Blueprint, jsonify, request
from app.models import PRODUCTS_DB, require_role

products_bp = Blueprint("products", __name__)


def validate_product(data, require_all=True):
    errors = {}
    if require_all or "name" in data:
        if not data.get("name"):
            errors["name"] = "Product name is required"
    if require_all or "price" in data:
        price = data.get("price")
        if price is None:
            errors["price"] = "Price is required"
        elif not isinstance(price, (int, float)) or price < 0:
            errors["price"] = "Price must be a non-negative number"
    if require_all or "stock" in data:
        stock = data.get("stock")
        if stock is None:
            errors["stock"] = "Stock is required"
        elif not isinstance(stock, int) or stock < 0:
            errors["stock"] = "Stock must be a non-negative integer"
    return errors


@products_bp.route("/", methods=["GET"])
@require_role("user", "moderator", "admin")
def list_products():
    return jsonify({"products": PRODUCTS_DB, "total": len(PRODUCTS_DB)}), 200


@products_bp.route("/<int:product_id>", methods=["GET"])
@require_role("user", "moderator", "admin")
def get_product(product_id):
    product = next((p for p in PRODUCTS_DB if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": f"Product {product_id} not found"}), 404
    return jsonify(product), 200


@products_bp.route("/", methods=["POST"])
@require_role("moderator", "admin")
def create_product():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_product(data, require_all=True)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 422

    new_id = max(p["id"] for p in PRODUCTS_DB) + 1 if PRODUCTS_DB else 1
    product = {
        "id": new_id, "name": data["name"],
        "price": data["price"], "stock": data["stock"]
    }
    PRODUCTS_DB.append(product)
    return jsonify({"message": "Product created", "product": product}), 201


@products_bp.route("/<int:product_id>", methods=["PUT"])
@require_role("moderator", "admin")
def update_product(product_id):
    product = next((p for p in PRODUCTS_DB if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": f"Product {product_id} not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_product(data, require_all=False)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 422

    product.update({k: data[k] for k in ("name", "price", "stock") if k in data})
    return jsonify({"message": "Product updated", "product": product}), 200


@products_bp.route("/<int:product_id>", methods=["DELETE"])
@require_role("admin")
def delete_product(product_id):
    idx = next((i for i, p in enumerate(PRODUCTS_DB) if p["id"] == product_id), None)
    if idx is None:
        return jsonify({"error": f"Product {product_id} not found"}), 404

    PRODUCTS_DB.pop(idx)
    return jsonify({"message": f"Product {product_id} deleted"}), 200
  
