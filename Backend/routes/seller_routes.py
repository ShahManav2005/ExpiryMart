from flask import Blueprint, request, jsonify, redirect ,session
from database.db import sellers, products , payments
from bson import ObjectId 
from datetime import datetime
from pricing import calculate_buying_price

seller_routes = Blueprint("seller_routes", __name__)

@seller_routes.route("/seller/signup", methods=["POST"])
def seller_signup():

    data = request.form

    seller = {
        "name": data.get("name"),
        "email": data.get("email"),
        "mobile": data.get("mobile"),
        "age": data.get("age"),
        "address": data.get("address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "pincode": data.get("pincode"),
        "id_proof": data.get("id_proof"),
        "password": data.get("password") 
    }

    result = sellers.insert_one(seller)
    session["seller_id"] = str(result.inserted_id)

    return jsonify({"message": "Seller account created successfully"})


#Add Product Route
@seller_routes.route("/seller/add-product", methods=["POST"])
def add_product():  
    data = request.form

    # ✅ Step 1 — Check session first, then fall back to form data
    seller_id = session.get("seller_id") or data.get("seller_id")
    if not seller_id:
        return jsonify({"error": "Please login first"}), 401

    # ✅ Step 2 — Validate expiry date
    expiry_str = data.get("expiry_date")
    if not expiry_str:
        return jsonify({"error": "Expiry date is required"}), 400

    expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
    days_left = (expiry - datetime.today()).days

    if days_left < 30:
        return jsonify({"error": "Expiry must be more than 1 month"}), 400

    # ✅ Step 3 — Now build product dict after all checks pass
    product = {
        "seller_id":    seller_id,
        "product_name": data.get("product_name"),
        "category":     data.get("category"),
        "details":      data.get("details"),
        "expiry_date":  expiry_str,
        "mrp":          data.get("mrp"),
        "quantity":     data.get("quantity"),
        "photo_count":  len(request.files.getlist("photos")),  # store count only
        "status":       "pending_payment"
    }

    # ✅ Step 4 — Insert only after all validations pass
    result = products.insert_one(product)
    product_id = str(result.inserted_id)

    return jsonify({
        "message": "Product submitted successfully",
        "product_id": product_id
    })
# Payment - API

@seller_routes.route("/seller/pay-inspection",methods=["POST"])
def pay_inspection():
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        seller_id = data.get("seller_id")

        if not product_id:
            return jsonify({"error": "product_id missing"}), 400

        # Fetch product to get MRP and expiry
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        mrp = float(product.get("mrp", 0))
        expiry_str = product.get("expiry_date")
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
        days_left = (expiry - datetime.today()).days
        months_left = days_left // 30

        # ✅ Buying price rule from pricing module
        buying_price = calculate_buying_price(mrp, months_left)

        # Update product
        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {
                "status": "inspection_pending",
                "buying_price": buying_price,
                "months_left": months_left
            }}
        )

        payments.insert_one({
            "seller_id": seller_id,
            "product_id": product_id,
            "amount": 100,
            "status": "paid",
            "paid_at": datetime.utcnow()
        })

        return jsonify({
            "message": "Payment successful",
            "buying_price": buying_price
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    
# inspection status API
@seller_routes.route("/seller/inspection-status", methods=["GET"])
def inspection_status():

    seller_id = request.args.get("seller_id")

    # fetch products for this seller
    seller_products = products.find({"seller_id": seller_id})

    result = []

    for p in seller_products:
        result.append({
            "product_name": p.get("product_name"),
            "category": p.get("category"),
            "expiry_date": p.get("expiry_date"),
            "status": p.get("status"),
            "comment": p.get("comment", "No comment")
        })

    return jsonify(result)