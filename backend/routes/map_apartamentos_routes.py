from flask import Blueprint, jsonify, request
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

map_apartamentos_routes = Blueprint("map_apartamentos_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@map_apartamentos_routes.route("/apartments", methods=["GET"])
def get_apartments():
    """
    Devuelve todos los apartamentos con coordenadas, si existen.
    """
    try:
        response = supabase.table("apartamentos").select("*").execute()
        data = response.data or []

        # Filtrar solo los que tienen latitud y longitud
        apartments = [
            {
                "id": a["id"],
                "titulo": a["titulo"],
                "barrio": a.get("barrio"),
                "precio": a.get("precio"),
                "direccion": a.get("direccion"),
                "descripcion": a.get("descripcion"),
                "tamaño_m2": a.get("tamaño_m2"),
                "amueblado": a.get("amueblado"),
                "disponible": a.get("disponible"),
                "latitud": a.get("latitud"),
                "longitud": a.get("longitud")
            }
            for a in data if a.get("latitud") and a.get("longitud")
        ]

        return jsonify(apartments), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@map_apartamentos_routes.route("/apartments/search", methods=["GET"])
def search_apartments():
    """
    Busca apartamentos filtrando por barrio y presupuesto.
    /apartments/search?barrio=Centro&presupuesto=900
    """
    try:
        barrio = request.args.get("barrio", type=str)
        presupuesto = request.args.get("presupuesto", type=float)

        query = supabase.table("apartamentos").select("*")

        if barrio:
            query = query.ilike("barrio", f"%{barrio}%")
        if presupuesto:
            query = query.lte("precio", presupuesto)

        response = query.execute()
        data = response.data or []

        apartments = [
            {
                "id": a["id"],
                "titulo": a["titulo"],
                "barrio": a.get("barrio"),
                "precio": a.get("precio"),
                "direccion": a.get("direccion"),
                "descripcion": a.get("descripcion"),
                "tamaño_m2": a.get("tamaño_m2"),
                "amueblado": a.get("amueblado"),
                "disponible": a.get("disponible"),
                "latitud": a.get("latitud"),
                "longitud": a.get("longitud")
            }
            for a in data if a.get("latitud") and a.get("longitud")
        ]

        return jsonify(apartments), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500