from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["expirymart"]

sellers = db["sellers"]
users = db["users"]
products = db["products"]
orders = db["orders"]
payments = db["payments"]
buyers = db["buyers"]
carts = db["carts"]