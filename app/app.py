from flask import Flask
from app.routes import setup_routes

app = Flask(__name__)

# Setup all routes from routes.py
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
