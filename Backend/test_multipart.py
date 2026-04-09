import requests

url = "http://localhost:5000/buyer/signup"
files = {
    'name': (None, 'Test Multipart Buyer'),
    'email': (None, 'test_multi@example.com'),
    'mobile': (None, '1234567890'),
    'age': (None, '20'),
    'address': (None, '123 Test St'),
    'city': (None, 'Testville'),
    'state': (None, 'TS'),
    'pincode': (None, '123456'),
    'password': (None, 'mypassword123')
}

response = requests.post(url, files=files)
print("Signup status:", response.status_code)
print("Signup response:", response.text)

# Now check DB directly
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["expirymart"]
buyers = db["buyers"]
b = buyers.find_one({"email": "test_multi@example.com"})
print("Password stored in DB:", b.get("password"))
