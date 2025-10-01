from flask import Flask
from backend.routes.chat_routes import chat_routes
from backend.routes.biomedical_routes import biomedical_routes
from backend.routes.map_clinics_routes import map_clinics_routes
from backend.routes.map_universities_routes import map_universities_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(chat_routes)
app.register_blueprint(biomedical_routes)
app.register_blueprint(map_clinics_routes)
app.register_blueprint(map_universities_routes)

if __name__ == "__main__":
    app.run(debug=True)