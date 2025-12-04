from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client
import requests
load_dotenv()

moving_routes = Blueprint("moving_routes", __name__)
CORS(moving_routes)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
ORS_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjAzNjA1M2RiMGZjYzQyZGFhZmYyMGU4ZWZjNTkwZmE3IiwiaCI6Im11cm11cjY0In0="  # OpenRouteService API Key

@moving_routes.route("/get_moving_companies", methods=["GET"])
def get_moving_companies():
    response = supabase.table("moving_companies").select("*").execute()

    companies = [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "cif": c.get("cif"),
            "base_fee": c.get("base_fee"),
            "price_small_package": c.get("price_small_package"),
            "price_medium_package": c.get("price_medium_package"),
            "price_large_package": c.get("price_large_package"),
            "price_solo_traslado": c.get("price_solo_traslado"),
            "price_mudanza": c.get("price_mudanza"),
            "price_mudanza_completa": c.get("price_mudanza_completa"),
            "rating": c.get("rating"),
            "location": c.get("location"),
            "estimated_time_days": c.get("estimated_time_days"),
            "max_weight_kg": c.get("max_weight_kg"),
            "km_price": c.get("km_price"),
            "phone": c.get("phone"),
            "email": c.get("email"),


            
        }
        for c in response.data
    ]

    if companies is None:
        # Something went wrong
        return jsonify({"error": "Could not fetch companies"}), 500

    return jsonify(companies)
BUCKET = "moving_companies"   # tu bucket real

@moving_routes.route("/get_company_images")
def get_company_images():
    company_id = request.args.get("id")

    if not company_id:
        return jsonify({"error": "Missing company id"}), 400

    try:
        res = supabase.table("moving_companies_images") \
                      .select("*") \
                      .eq("company_id", int(company_id)) \
                      .execute()

        images = res.data or []

        # Transform image paths into full Supabase public URLs
        for img in images:
            if img.get("image_url"):
                img["image_url"] = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{img['image_url']}"

        return jsonify(images)

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    
@moving_routes.route("/calc_distance", methods=["GET"])
def calc_distance():
    # 1. Validación de la Clave API
    if not ORS_KEY:
        return jsonify({"error": "ORS API Key is not configured (ORS_API_KEY missing in environment)."}), 500

    # 2. Obtención y Validación de Parámetros
    origin = request.args.get("from")
    destination = request.args.get("to")

    if not origin or not destination:
        # Se ha omitido "from" o "to" en la URL
        return jsonify({"error": "Missing parameters. Please provide 'from' (origin) and 'to' (destination)."}), 400

    # 3. Función Auxiliar para Geocodificación (para reducir la duplicación de código)
    def geocode_location(location_str):
        try:
            geo_res = requests.get(
                "https://api.openrouteservice.org/geocode/search",
                params={"api_key": ORS_KEY, "text": location_str},
                timeout=10 # Buena práctica: establecer un tiempo de espera
            )
            geo_res.raise_for_status() # Lanza HTTPError si el código de estado es 4xx o 5xx
            geo_data = geo_res.json()

            if not geo_data.get("features"):
                return None, f"No se encontró una ubicación válida para: '{location_str}'"

            # OpenRouteService usa [longitud, latitud]
            lon, lat = geo_data["features"][0]["geometry"]["coordinates"]
            return (lon, lat), None

        except requests.exceptions.RequestException as e:
            # Manejo de errores de conexión o HTTP
            return None, f"Fallo en la geocodificación para '{location_str}': {e}"
        except Exception as e:
             # Manejo de otros errores (como problemas de parseo JSON)
             return None, f"Error inesperado al geocodificar '{location_str}': {e}"

    # ---------- GEOCODING ORIGEN y DESTINO ----------
    (lon_o, lat_o), error_o = geocode_location(origin)
    if error_o:
        return jsonify({"error": "Error de origen", "details": error_o}), 400
    
    (lon_d, lat_d), error_d = geocode_location(destination)
    if error_d:
        return jsonify({"error": "Error de destino", "details": error_d}), 400

    # ---------- SOLICITUD DE DISTANCIA (RUTEO) ----------
    directions_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    try:
        # La clave API DEBE ir en el encabezado 'Authorization' para el ruteo.
        route_res = requests.post(
            directions_url,
            json={"coordinates": [[lon_o, lat_o], [lon_d, lat_d]]},
            headers={
                # Uso correcto: La clave API va aquí según la documentación de ORS para POST
                "Authorization": ORS_KEY, 
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=15
        )
        route_res.raise_for_status() # Lanza HTTPError para errores de ruteo
        route_data = route_res.json()

        # 4. Extracción y Formato del Resultado
        # La distancia está en metros
        distance_m = route_data["routes"][0]["summary"]["distance"]
        distance_km = round(distance_m / 1000, 1)
        
        # Opcional: obtener la duración
        duration_s = route_data["routes"][0]["summary"]["duration"]
        duration_min = round(duration_s / 60)

        return jsonify({
            "origin": origin,
            "destination": destination,
            "distance_km": distance_km,
            "duration_minutes": duration_min,
            "api_source": "OpenRouteService"
        })

    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión o HTTP
        return jsonify({"error": "Fallo en la solicitud de ruteo", "details": str(e)}), 500
    except KeyError:
        # Si la estructura JSON no es la esperada (ej. no hay 'routes')
         return jsonify({
             "error": "Ruteo fallido. Respuesta API inesperada.", 
             "api_response": route_data.get('error', 'No se encontró el campo "routes"') 
         }), 500
    except Exception as e:
        # Errores inesperados
        return jsonify({"error": "Error inesperado al rutear", "details": str(e)}), 500
    
@moving_routes.route("/validate_address")
def validate_address():
    city = request.args.get("city")
    import requests

    url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={city}"
    res = requests.get(url).json()

    exists = len(res.get("features", [])) > 0

    return jsonify({"valid": exists})

@moving_routes.route("/fetch_company_reviews")
def fetch_company_reviews():
    company_id = request.args.get("id")

    if not company_id:
        return jsonify({"error": "Missing company id"}), 400

    try:
        res = supabase.table("reviews_moving_companies") \
                      .select("*") \
                      .eq("company_id", int(company_id)) \
                      .execute()

        return jsonify(res.data or [])

    except Exception as e:
        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500
@moving_routes.route("/submit_company_review", methods=["POST", "OPTIONS"])
def submit_company_review():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    data = request.get_json()

    company_id = data.get("company_id")
    user_id = data.get("user_id")
    date=data.get("date")
    service_type=data.get("service_type")   
    rating = data.get("rating")
    comment = data.get("comment")

    if not all([company_id, user_id, rating, comment, date, service_type]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        res = supabase.table("reviews_moving_companies").insert({
            "company_id": company_id,
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "review_date": date,
            "service_type": service_type
        }).execute()

        return jsonify({"message": "Review submitted successfully", "data": res.data}), 201
    except Exception as e:
        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500
    
