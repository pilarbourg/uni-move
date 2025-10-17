from flask import Blueprint, jsonify
import requests

libraries_routes = Blueprint("libraries_routes", __name__)

@libraries_routes.route("/api/libraries")
def get_libraries():
    api_url = "https://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.json"
    response = requests.get(api_url)
    data = response.json()
    print(data["@graph"][0].keys())
    
    libraries = []
    for lib in data.get("@graph", []):
        libraries.append({
            "name": lib.get("title"),
            "latitude": lib.get("location", {}).get("latitude"),
            "longitude": lib.get("location", {}).get("longitude"),
            "address": {
                "street": lib.get("address", {}).get("street-address"),
                "postal_code": lib.get("address", {}).get("postal-code"),
                "locality": lib.get("address", {}).get("locality"),
                "area": lib.get("address", {}).get("area"),
            },
            "services": lib.get("organization", {}).get("services"),
            "accessibility": lib.get("organization", {}).get("accesibility"),
            "description": lib.get("description") or lib.get("organization", {}).get("organization-desc"),
            "link": lib.get("link"),
            "event_info": {
                "recurrence": lib.get("recurrence"),
                "dtstart": lib.get("dtstart"),
                "dtend": lib.get("dtend"),
            }
        })
    
    return jsonify(libraries)