from flask import Blueprint ,jsonify ,request
from database.db import products
from bson import ObjectId
from pricing import calculate_buying_price

inspector_routes = Blueprint("inspector_routes", __name__)

# Dashbord API (Fetch Pending Products)
@inspector_routes.route("/inspector/dashboard", methods=["GET"])
def inspector_dashboard():

    data = products.find({"status": "inspection_pending"})

    result = []

    for p in data:
        result.append({
            "id": str(p["_id"]),
            "seller_id": p.get("seller_id"),
            "product_name": p.get("product_name"),
            "category": p.get("category"),
            "expiry_date": p.get("expiry_date"),
            "mrp": p.get("mrp"),
            "quantity": p.get("quantity")
        })

    return jsonify(result)

# Approve Product
@inspector_routes.route("/inspector/approve/<product_id>", methods=["POST"])
def approve_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Use existing buying_price, or calculate it now if not set
        buying_price = product.get("buying_price")
        if not buying_price:
            mrp = float(product.get("mrp") or 0)
            expiry_str = product.get("expiry_date")
            if mrp and expiry_str:
                from datetime import datetime
                expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
                days_left = (expiry - datetime.today()).days
                months_left = max(1, days_left // 30)
                buying_price = calculate_buying_price(mrp, months_left)
            else:
                buying_price = 0

        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {
                "status":        "approved",
                "buying_price":  buying_price,
                "comment":       "Approved by inspector"
            }}
        )

        return jsonify({
            "message":       "Product approved",
            "buying_price":  buying_price
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Reject Product
@inspector_routes.route("/inspector/reject/<product_id>", methods=["POST"])
def reject_product(product_id):
    data = request.get_json() or {}
    comment = data.get("comment", "Rejected by inspector")

    products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {
            "status": "rejected",
            "comment": comment
        }}
    )

    return jsonify({"message": "Product rejected"})