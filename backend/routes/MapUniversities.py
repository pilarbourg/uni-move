import requests
import json
import folium

# Consulta Overpass: universidades en España
query = """
[out:json];
area["ISO3166-1"="ES"][admin_level=2];
node["amenity"="university"](40.2,-4.5,41.1,-3.0);
out;
"""

url = "https://overpass-api.de/api/interpreter"

response = requests.post(url, data={"data": query})

if response.status_code == 200:
    data = response.json()  # El JSON ya convertido en diccionario Python
    for element in data["elements"]:
        name = element.get("tags", {}).get("name", "Desconocida")
        lat = element.get("lat")
        lon = element.get("lon")
        print(f"{name} -> {lat}, {lon}")
else:
    print("Error en la petición:", response.status_code)

class Universidad:
    def __init__(self, nombre, lat, lon):
        self.nombre = nombre
        self.lat = lat
        self.lon = lon

universidades = []

for element in data["elements"]:
    name = element.get("tags", {}).get("name", "Desconocida")
    lat = element.get("lat")
    lon = element.get("lon")
    universidades.append(Universidad(name, lat, lon))


# Crear mapa centrado en España
m = folium.Map(location=[40.4, -3.7], zoom_start=6)

# Añadir universidades como marcadores
for u in universidades:
    folium.Marker(
        location=[u.lat, u.lon],
        popup=u.nombre
    ).add_to(m)

# Guardar en HTML y abrir en navegador
m.save("frontend/pages/universidades.html")
