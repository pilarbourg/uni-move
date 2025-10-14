# backend/routes/map_apartamentos_routes.py
from flask import Blueprint, request, jsonify
from backend.apartamentos_info.apartamentos import (
    listar_apartamentos,
    buscar_precio,
    buscar_barrio_precio,
)

# MISMA IDEA QUE EN UNIVERSITIES: blueprint sin url_prefix
map_apartamentos_routes = Blueprint("map_apartamentos_routes", __name__)

@map_apartamentos_routes.route("/get_apartamentos", methods=["GET"])
def get_apartamentos():
    """Devuelve todos los apartamentos"""
    data = listar_apartamentos()
    return jsonify(_normalize(data)), 200

@map_apartamentos_routes.route("/get_apartamentos_by_price/<int:presupuesto>", methods=["GET"])
def get_apartamentos_by_price(presupuesto: int):
    """Filtra por presupuesto máximo (≤)"""
    data = buscar_precio(float(presupuesto))
    return jsonify(_normalize(data)), 200

@map_apartamentos_routes.route("/get_apartamentos_by_neighborhood_and_price", methods=["GET"])
def get_apartamentos_by_neighborhood_and_price():
    """
    Filtra por barrio (ilike) y presupuesto (≤)
    Ejemplo:
      /get_apartamentos_by_neighborhood_and_price?barrio=Centro&presupuesto=1200
    """
    barrio = (request.args.get("barrio") or "").strip()
    presupuesto = request.args.get("presupuesto", type=float)
    if not barrio or presupuesto is None:
        return jsonify({"error": "barrio y presupuesto son requeridos"}), 400
    data = buscar_barrio_precio(barrio, float(presupuesto))
    return jsonify(_normalize(data)), 200


# ---- util: normaliza tipos a number para el front (lat/lon/precio/metros) ----
def _normalize(rows):
    out = []
    for a in rows or []:
        d = dict(a)
        for k in ("latitude", "longitude", "precio", "tamano_m2"):
            if k in d and d[k] is not None and isinstance(d[k], str):
                try:
                    d[k] = float(d[k])
                except Exception:
                    pass
        out.append(d)
    return out
