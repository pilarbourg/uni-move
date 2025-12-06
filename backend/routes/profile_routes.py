from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from supabase import create_client, Client

profile_routes = Blueprint("profile_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@profile_routes.route("/api/update_profile", methods=["PUT", "POST", "OPTIONS"])
@cross_origin()
def update_profile():
    """Endpoint para actualizar el perfil del usuario"""
    
    # Manejar preflight requests
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    try:
        # Obtener datos
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        email = data.get("email")
        
        if not email:
            return jsonify({"message": "Email es requerido"}), 400
        
        # Verificar si el usuario existe
        result = supabase.table("users").select("*").eq("email", email).execute()
        
        if not result.data:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Preparar campos a actualizar
        update_data = {}
        
        if "profile_name" in data:
            update_data["profile_name"] = data.get("profile_name")
        if "nationality" in data:
            update_data["nationality"] = data.get("nationality")
        if "hobby" in data:
            update_data["hobby"] = data.get("hobby")
        
        if not update_data:
            return jsonify({"message": "No hay datos para actualizar"}), 400
        
        # Actualizar en la base de datos
        response = supabase.table("users").update(update_data).eq("email", email).execute()
        
        return jsonify({
            "message": "Perfil actualizado exitosamente",
            "updated_fields": update_data,
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@profile_routes.route("/api/get_profile", methods=["GET"])
@cross_origin()
def get_profile():
    """Endpoint para obtener datos del perfil"""
    email = request.args.get("email")
    
    if not email:
        return jsonify({"message": "Email es requerido"}), 400
    
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        
        if not result.data:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        user = result.data[0]
        return jsonify({
            "email": user.get("email"),
            "profile_name": user.get("profile_name"),
            "nationality": user.get("nationality"),
            "hobby": user.get("hobby")
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
