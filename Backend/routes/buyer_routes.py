from flask import Blueprint, request, jsonify , redirect
from database.db import buyers , products, carts
from bson import ObjectId
from datetime import datetime
from pricing import calculate_selling_price

buyer_routes = Blueprint("buyer_routes", __name__)

@buyer_routes.route("/buyer/signup", methods=["POST"])
def buyer_signup():

    data = request.form

    buyer = {
        "name": data.get("name"),
        "email": data.get("email"),
        "mobile": data.get("mobile"),
        "age": data.get("age"),
        "address": data.get("address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "pincode": data.get("pincode"),
        "password": data.get("password")
    }

    buyers.insert_one(buyer)

    return jsonify({"message": "Buyer account created successfully"})


    
@buyer_routes.route('/buyer/products', methods=['GET'])
def get_products():

    all_products = list(products.find({"status": "approved"}))
    result = []

    for p in all_products:

        expiry = p.get("expiry_date") or p.get("expiry")
        if not expiry:
            continue

        if isinstance(expiry, str):
            expiry = datetime.strptime(expiry, "%Y-%m-%d")

        days_left = (expiry - datetime.today()).days
        months_left = days_left // 30

        # ❌ Old wrong code:
        # price = p.get("buying_price") or p.get("price") or 0

        # ✅ Fix: use buying_price set during inspection payment
        buying_price = p.get("buying_price")
        if not buying_price:
            continue   # skip products without buying price

        buying_price = float(buying_price)

        # ✅ Use correct selling price formula
        selling_price = calculate_selling_price(buying_price, months_left)

        result.append({
            "id": str(p["_id"]),
            "name": p.get("product_name") or p.get("name"),
            "category": p.get("category"),
            "expiry": expiry.strftime("%Y-%m-%d"),
            "mrp": p.get("mrp"),
            "buying_price": buying_price,
            "selling_price": selling_price,    # ← this is what buyer sees
            "months_left": months_left
        })

    return jsonify(result)


@buyer_routes.route('/buyer/buy/<product_id>', methods=['POST'])
def buy_product(product_id):
    try:
        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"status": "sold"}}
        )
        return jsonify({"message": "Order placed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@buyer_routes.route('/buyer/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    buyer_id = data.get("buyer_id")
    product_id = data.get("product_id")

    if not buyer_id or not product_id:
        return jsonify({"error": "Missing buyer_id or product_id"}), 400

    product = products.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_item = {
        "buyer_id": buyer_id,
        "product_id": product_id,
        "added_at": datetime.utcnow()
    }
    carts.insert_one(cart_item)
    return jsonify({"message": "Added to cart successfully!"})

@buyer_routes.route('/buyer/cart/<buyer_id>', methods=['GET'])
def get_cart(buyer_id):
    cart_items = list(carts.find({"buyer_id": buyer_id}))
    result = []
    
    for item in cart_items:
        product_id = item.get("product_id")
        p = products.find_one({"_id": ObjectId(product_id)})
        if not p:
            continue
            
        expiry = p.get("expiry_date") or p.get("expiry")
        if not expiry: continue
        if isinstance(expiry, str):
            expiry = datetime.strptime(expiry, "%Y-%m-%d")
            
        days_left = (expiry - datetime.today()).days
        months_left = days_left // 30
        buying_price = p.get("buying_price")
        if not buying_price: continue
        buying_price = float(buying_price)
        selling_price = calculate_selling_price(buying_price, months_left)

        result.append({
            "cart_id": str(item["_id"]),
            "product_id": str(p["_id"]),
            "name": p.get("product_name") or p.get("name"),
            "category": p.get("category"),
            "expiry": expiry.strftime("%Y-%m-%d"),
            "mrp": p.get("mrp"),
            "selling_price": selling_price,
            "days_left": max(0, days_left)
        })

    return jsonify(result)

@buyer_routes.route('/buyer/cart/remove/<cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        carts.delete_one({"_id": ObjectId(cart_id)})
        return jsonify({"message": "Item removed from cart"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500