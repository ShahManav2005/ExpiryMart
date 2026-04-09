import urllib.request
import urllib.parse
import uuid

# Create multipart data
boundary = uuid.uuid4().hex
fields = {
    "name": "Multipart Buyer",
    "email": "multi@example.com",
    "mobile": "123",
    "age": "20",
    "address": "123",
    "city": "Test",
    "state": "TS",
    "pincode": "123",
    "password": "mypassword123"
}

body = []
for key, value in fields.items():
    body.extend([
        f'--{boundary}',
        f'Content-Disposition: form-data; name="{key}"',
        '',
        value
    ])
body.extend([f'--{boundary}--', ''])
data = '\r\n'.join(body).encode('utf-8')

req = urllib.request.Request("http://localhost:5000/buyer/signup", data=data)
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

try:
    with urllib.request.urlopen(req) as response:
        print("Response:", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
    
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["expirymart"]
buyers = db["buyers"]
b = buyers.find_one({"email": "multi@example.com"})
print("Saved password:", b.get("password"))
