from flask import Flask
from flask_cors import CORS  # Import CORS
from app.routes import setup_routes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

setup_routes(app)

if __name__ != "__main__":
    application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
