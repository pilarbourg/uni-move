from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import math
import os
from supabase import create_client
import folium

app = Flask(__name__)
load_dotenv()

map_universities_routes = Blueprint("map_universities_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@map_universities_routes.route("/get_universities", methods=["GET"])
def get_universities():
    response = supabase.table("universities").select("*").execute()

    universities = [
        {
            "id": u.get("id"),
            "name": u.get("name"),
            "latitude": u.get("latitude"),
            "longitude": u.get("longitude"),
        }
        for u in response.data
    ]

    if universities is None:
        # Something went wrong
        return jsonify({"error": "Could not fetch universities"}), 500

    return jsonify(universities)
if __name__ == "__main__":
    app.run(debug=True)
print("Mapa generado: mapa_universidades_madrid.html")