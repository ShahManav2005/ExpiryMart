from database.db import products
from datetime import datetime

def create_product(data):

    product = {
        # "seller_id": data.get("seller_id"),
        "product_name": data.get("product_name"),
        "category": data.get("category"),
        "details": data.get("details"),
        "expiry_date": data.get("expiry_date"),
        "mrp": data.get("mrp"),
        "quantity": data.get("quantity"),
        "photos": [data.get("photos")],
        "status": "pending_payment",
        "created_at": datetime.utcnow()
    }

    return products.insert_one(product)