from flask import Flask
from backend.routes.chat_routes import chat_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(chat_routes)

if __name__ == "__main__":
    app.run(debug=True)