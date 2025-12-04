from flask import Flask
from backend.routes.profile_routes import profile_routes
from backend.routes.chat_routes import chat_routes
from backend.routes.bio_profile_routes import bio_profile_routes
from backend.routes.illnesses_routes import illness_routes
from backend.routes.map_apartamentos_routes import map_apartamentos_routes
from backend.routes.map_clinics_routes import map_clinics_routes
from backend.routes.map_universities_routes import map_universities_routes
from backend.routes.login_routes import login_routes
from backend.routes.university_search_routes import university_search_routes
from backend.routes.medical_contacts_routes import medical_contacts_routes
from backend.routes.related_degrees_routes import related_degrees_routes
from backend.routes.uni_contact_routes import contact_routes
from backend.routes.universities.libraries_external import libraries_routes
from backend.routes.medical_reminders_routes import medical_reminders_routes
from backend.routes.universities.libraries_review import libraries_reviews_routes
from backend.routes.moving_routes import moving_routes
from backend.routes.events import events_routes
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

app.register_blueprint(profile_routes)
app.register_blueprint(chat_routes)
app.register_blueprint(bio_profile_routes)
app.register_blueprint(illness_routes)
app.register_blueprint(map_clinics_routes)
app.register_blueprint(map_universities_routes)
app.register_blueprint(login_routes)
app.register_blueprint(university_search_routes)
app.register_blueprint(related_degrees_routes)
app.register_blueprint(contact_routes)
app.register_blueprint(map_apartamentos_routes)
app.register_blueprint(medical_contacts_routes)
app.register_blueprint(medical_reminders_routes)
app.register_blueprint(libraries_routes)
app.register_blueprint(libraries_reviews_routes)
app.register_blueprint(moving_routes)
app.register_blueprint(events_routes)


print("\n=== ROUTES ===")
for rule in app.url_map.iter_rules():
    print(rule)
print("================\n")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)