from flask import Blueprint, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

events_routes = Blueprint("events_routes", __name__)

TM_API_KEY = os.getenv("TM_API_KEY")

@events_routes.route("/api/events-madrid", methods=["GET"])
def get_events():
    if not TM_API_KEY:
        return jsonify({"error": "Missing TM_API_KEY in .env"}), 500

    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&city=Madrid&size=200"

    res = requests.get(url)

    if res.status_code != 200:
        return jsonify({"error":"Ticketmaster request failed"}), res.status_code

    return jsonify(res.json())
