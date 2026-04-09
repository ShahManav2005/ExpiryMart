from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["expirymart"]
buyers = db["buyers"]

all_b = list(buyers.find())
print(f"Total buyers: {len(all_b)}")
for b in all_b:
    print(f"Email: {b.get('email')}, Password: '{b.get('password')}'")
