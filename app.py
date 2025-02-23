from flask import Flask
from app.routes import setup_routes  # Ensure this matches your folder structure

app = Flask(__name__)  # ✅ Ensure this is correctly defined

setup_routes(app)  # Registers the routes

if __name__ != "__main__":  # Gunicorn expects the app instance
    application = app  # ✅ Add this line

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
