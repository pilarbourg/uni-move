from flask import Blueprint, jsonify
import requests
import json
import folium

map_universities_routes = Blueprint("map_universities_routes", __name__)

def generate_universities_map():
    query = """
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    node["amenity"="university"](40.2,-4.5,41.1,-3.0);
    out;
    """
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})

    if response.status_code != 200:
        return f"Error en la petición: {response.status_code}"

    data = response.json()

    class Universidad:
        def __init__(self, nombre, lat, lon):
            self.nombre = nombre
            self.lat = lat
            self.lon = lon

    universidades = [
        Universidad(
            element.get("tags", {}).get("name", "Desconocida"),
            element.get("lat"),
            element.get("lon")
        )
        for element in data["elements"]
    ]

    m = folium.Map(location=[40.4, -3.7], zoom_start=6)

    for u in universidades:
        folium.Marker(location=[u.lat, u.lon], popup=u.nombre).add_to(m)

    m.save("frontend/pages/universidades.html")
    return "Mapa generado exitosamente"

@map_universities_routes.route("/api/generate_map", methods=["GET"])
def generate_map_route():
    result = generate_universities_map()
    return jsonify({"message": result})