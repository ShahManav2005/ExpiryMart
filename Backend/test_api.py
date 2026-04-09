import urllib.request
import urllib.parse
import json

# 1. Signup Buyer
signup_url = "http://localhost:5000/buyer/signup"
data = urllib.parse.urlencode({
    "name": "Test Buyer",
    "email": "test_buyer1@example.com",
    "mobile": "1234567890",
    "age": "20",
    "address": "123 Test St",
    "city": "Testville",
    "state": "TS",
    "pincode": "123456",
    "password": "mypassword123"
}).encode("utf-8")

req = urllib.request.Request(signup_url, data=data)
try:
    with urllib.request.urlopen(req) as response:
        print("Signup Response:", response.read().decode("utf-8"))
except Exception as e:
    print("Signup Error:", e)

# 2. Login Buyer
login_url = "http://localhost:5000/login"
login_data = json.dumps({
    "email": "test_buyer1@example.com",
    "password": "mypassword123",
    "role": "buyer"
}).encode("utf-8")

headers = {"Content-Type": "application/json"}
req2 = urllib.request.Request(login_url, data=login_data, headers=headers)
try:
    with urllib.request.urlopen(req2) as response:
        print("Login Response:", response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("Login Error:", e.read().decode("utf-8"))
