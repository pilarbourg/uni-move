import requests
import time
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, jsonify

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

IDEALISTA_API_KEY = os.getenv("IDEALISTA_API_KEY")
IDEALISTA_API_SECRET = os.getenv("IDEALISTA_API_SECRET")

class IdealistaAPI:
    def __init__(self, token_file="idealista_token.json"):
        self.client_id = IDEALISTA_API_KEY
        self.client_secret = IDEALISTA_API_SECRET
        self.token_file = token_file
        self.token = None
        self.token_expiry = 0
        self._load_token_from_file()

    def create_routes(self):
        bp = Blueprint("idealista", __name__, url_prefix="/idealista")
        @bp.route("/properties")
        def get_properties():
            cards = self.search_properties("40.430,-3.702")
            return jsonify(cards)

        return bp

    def _load_token_from_file(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                data = json.load(f)
                self.token = data.get("access_token")
                self.token_expiry = data.get("expiry", 0)

    def _save_token_to_file(self):
        with open(self.token_file, "w") as f:
            json.dump({
                "access_token": self.token,
                "expiry": self.token_expiry
            }, f)

    def _get_token(self):
        url = "https://api.idealista.com/oauth/token"
        data = {"grant_type": "client_credentials"}

        print("DEBUG: Getting token with:")
        print("URL:", url)
        print("Data:", data)
        print("Client ID:", self.client_id)
        print("Client Secret:", self.client_secret)

        response = requests.post(url, data=data, auth=(self.client_id, self.client_secret))
        
        print("DEBUG: Response status code:", response.status_code)
        print("DEBUG: Response text:", response.text)

        response.raise_for_status()
        token_info = response.json()
        self.token = token_info["access_token"]
        self.token_expiry = time.time() + token_info["expires_in"]
        self._save_token_to_file()

    def _ensure_token(self):
        if not self.token or time.time() >= self.token_expiry:
            self._get_token()

    def search_properties(self, center, property_type="homes", distance=15000, operation="rent"):
        try:
            self._ensure_token()
        except requests.HTTPError as e:
            print("Failed to get token:", e)
            raise

        url = "https://api.idealista.com/3.5/es/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "center": center,
            "propertyType": property_type,
            "distance": distance,
            "operation": operation
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        json_data = response.json()
        properties = json_data.get("elementList", [])

        cards = []
        for prop in properties:
            card = {
                "thumbnail": prop.get("thumbnail"),
                "title": prop.get("suggestedTexts", {}).get("title", prop.get("address")),
                "price": f"{prop['priceInfo']['price']['amount']} {prop['priceInfo']['price']['currencySuffix']}",
                "rooms": prop.get("rooms"),
                "bathrooms": prop.get("bathrooms"),
                "size": prop.get("size"),
                "url": prop.get("url"),
                "latitude": prop.get("latitude"),
                "longitude": prop.get("longitude"),
            }
            cards.append(card)

        return cards