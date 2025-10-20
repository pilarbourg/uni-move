from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

map_apartamentos_routes = Blueprint("map_apartamentos_routes", __name__)
CORS(map_apartamentos_routes)  # CORS para estas rutas

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def _normalize_apartment_row(a: dict) -> dict:


    tamano = a.get("tamano_m2", a.get("tamaño_m2"))
    return {
        "id": a.get("id"),
        "titulo": a.get("titulo"),
        "descripcion": a.get("descripcion"),
        "direccion": a.get("direccion"),
        "barrio": a.get("barrio"),
        "precio": a.get("precio"),
        "tamano_m2": tamano,
        "amueblado": a.get("amueblado"),
        "disponible": a.get("disponible"),
        "latitud": a.get("latitud", a.get("latitude")),
        "longitud": a.get("longitud", a.get("longitude")),
    }


@map_apartamentos_routes.route("/get_apartments", methods=["GET"])
def get_apartments():
    res = supabase.table("apartamentos").select("*").execute()
    data = [ _normalize_apartment_row(a) for a in (res.data or []) ]
    return jsonify(data)

@map_apartamentos_routes.route("/get_apartments_by_price/<float:presupuesto>", methods=["GET"])
def get_apartments_by_price(presupuesto: float):
    res = (
        supabase.table("apartamentos")
        .select("*")
        .lte("precio", presupuesto)
        .execute()
    )
    data = [ _normalize_apartment_row(a) for a in (res.data or []) ]
    return jsonify(data)

@map_apartamentos_routes.route("/get_apartments_by_barrio/<string:barrio>", methods=["GET"])
def get_apartments_by_barrio(barrio: str):
    res = (
        supabase.table("apartamentos")
        .select("*")
        .ilike("barrio", f"%{barrio}%")
        .execute()
    )
    data = [ _normalize_apartment_row(a) for a in (res.data or []) ]
    return jsonify(data)

@map_apartamentos_routes.route("/get_apartments_by_barrio_price", methods=["GET"])
def get_apartments_by_barrio_price():
    barrio = request.args.get("barrio", "")
    presupuesto = request.args.get("presupuesto", type=float)
    q = supabase.table("apartamentos").select("*")
    if barrio:
        q = q.ilike("barrio", f"%{barrio}%")
    if presupuesto is not None:
        q = q.lte("precio", presupuesto)
    res = q.execute()
    data = [ _normalize_apartment_row(a) for a in (res.data or []) ]
    return jsonify(data)
