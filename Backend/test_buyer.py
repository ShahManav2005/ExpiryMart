from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["expirymart"]
buyers = db["buyers"]

for b in buyers.find():
    print(f"Email: {b.get('email')}, Password: '{b.get('password')}'")
