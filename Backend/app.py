import os
from flask import Flask
from flask_cors import CORS
from routes.seller_routes import seller_routes
from routes.buyer_routes import buyer_routes          # explicit import
from routes.inspector_routes import inspector_routes
from routes.product_routes import product_routes
from routes.auth_routes import auth

app = Flask(__name__)
app.secret_key = "expirymart123"

CORS(app, supports_credentials=True, origins="*")

app.register_blueprint(product_routes)
app.register_blueprint(inspector_routes)
app.register_blueprint(seller_routes)
app.register_blueprint(buyer_routes)
app.register_blueprint(auth)

@app.route("/")
def home():
    return {"message": "ExpiryMart Backend Running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)