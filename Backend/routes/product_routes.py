from flask import Blueprint, request, jsonify
from database.db import products
from bson import ObjectId

product_routes = Blueprint("product_routes", __name__)

# Get Products (Buyer + Inspector)
@product_routes.route("/products", methods=["GET"])
def get_products():

    result = list(products.find())

    for p in result:
        p["_id"] = str(p["_id"])

    return jsonify(result)

# Product API
@product_routes.route("/product/<id>", methods=["GET"])
def get_product(id):

    product = products.find_one({"_id": ObjectId(id)})

    if not product:
        return jsonify({"error": "Product not found"}), 404
    product["_id"] = str(product["_id"])
    return jsonify(product)