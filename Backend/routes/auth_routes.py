from flask import Blueprint, request, jsonify, session
from database.db import sellers, buyers, users
from datetime import datetime

auth = Blueprint("auth", __name__)

# -----------------------------------------------
# SIGNUP — generic (stores in users collection)
# -----------------------------------------------
@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    name     = data.get("name")
    email    = data.get("email")
    password = data.get("password")
    role     = data.get("role")

    # Validate all fields present
    if not name or not email or not password or not role:
        return jsonify({"error": "All fields are required"}), 400

    # Check if email already exists
    existing = users.find_one({"email": email})
    if existing:
        return jsonify({"error": "Email already registered"}), 409

    users.insert_one({
        "name":       name,
        "email":      email,
        "password":   password,   # hash this later
        "role":       role,
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "User created successfully"})


# -----------------------------------------------
# LOGIN
# -----------------------------------------------
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email    = data.get("email")
    password = data.get("password")
    role     = data.get("role")

    if not email or not password or not role:
        return jsonify({"error": "All fields required"}), 400

    # Pick collection based on role
    if role == "buyer":
        collection = buyers
    elif role == "seller":
        collection = sellers
    else:
        return jsonify({"error": "Invalid role for now"}), 400

    # Find user
    user = collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "No account found with this email"}), 404

    # ✅ Check password
    stored_password = user.get("password")
    
    if not stored_password:
        return jsonify({"error": "This account is incomplete (missing password). Please sign up again."}), 401

    if stored_password != password:
        return jsonify({"error": "Incorrect password"}), 401

    # Save session
    session["user_id"] = str(user["_id"])
    session["role"]    = role
    session["email"]   = email

    # Also store role-specific ID so seller_routes / buyer_routes can find it
    if role == "seller":
        session["seller_id"] = str(user["_id"])
    elif role == "buyer":
        session["buyer_id"] = str(user["_id"])

    return jsonify({
        "message":  "Login successful",
        "role":     role,
        "name":     user.get("name"),
        "user_id":  str(user["_id"])
    })


# -----------------------------------------------
# LOGOUT
# -----------------------------------------------
@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


