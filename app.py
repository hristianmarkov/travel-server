from flask import Flask
from app.routes import setup_routes  # This works since "routes.py" is inside the /app folder

app = Flask(__name__)

# Setup all routes from routes.py
setup_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)  # Ensure it runs on port 8080 for Railway
