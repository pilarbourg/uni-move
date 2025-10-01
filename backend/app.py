from flask import Flask
from backend.routes.chat_routes import chat_routes
from backend.routes.bio_profile_routes import bio_profile_routes
from backend.routes.map_clinics_routes import map_clinics_routes
from backend.routes.map_universities_routes import map_universities_routes
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_routes)
app.register_blueprint(bio_profile_routes)
app.register_blueprint(map_clinics_routes)
app.register_blueprint(map_universities_routes)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)