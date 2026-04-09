from database.db import sellers
from datetime import datetime

def create_seller(data):

    seller = {
        "name": data["name"],
        "email": data["email"],
        "mobile": data["mobile"],
        "age": data["age"],
        "address": data["address"],
        "city": data["city"],
        "state": data["state"],
        "pincode": data["pincode"],
        "id_proof": data["id_proof"],
        "created_at": datetime.utcnow()
    }

    return sellers.insert_one(seller)