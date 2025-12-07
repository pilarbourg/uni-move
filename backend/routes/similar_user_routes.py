from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from supabase import create_client, Client

similar_users_routes = Blueprint("similar_users_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@similar_users_routes.route("/api/get_similar_users/<email>", methods=["GET"])
@cross_origin()
def get_similar_users(email):
    """Endpoint para obtener usuarios con mismos hobbies o nacionalidad"""
    try:
        # 1. Obtener los datos del usuario actual
        current_user_result = supabase.table("users").select("*").eq("email", email).execute()
        
        if not current_user_result.data:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        current_user = current_user_result.data[0]
        current_hobby = current_user.get("hobby")
        current_nationality = current_user.get("nationality")
        
        # Si no tiene hobby ni nacionalidad, no hay usuarios similares
        if not current_hobby and not current_nationality:
            return jsonify({
                "message": "Usuario no tiene hobby o nacionalidad registrados",
                "similar_users": []
            }), 200
        
        # 2. Buscar usuarios similares (excluyendo al actual)
        similar_users = []
        
        # Buscar por hobby
        if current_hobby:
            hobby_users = supabase.table("users") \
                .select("email, profile_name, nationality, hobby") \
                .eq("hobby", current_hobby) \
                .neq("email", email) \
                .execute()
            
            for user in hobby_users.data:
                user["match_type"] = "hobby"
                similar_users.append(user)
        
        # Buscar por nacionalidad
        if current_nationality:
            nationality_users = supabase.table("users") \
                .select("email, profile_name, nationality, hobby") \
                .eq("nationality", current_nationality) \
                .neq("email", email) \
                .execute()
            
            for user in nationality_users.data:
                # Evitar duplicados si ya fue agregado por hobby
                if not any(u["email"] == user["email"] for u in similar_users):
                    user["match_type"] = "nationality"
                    similar_users.append(user)
        
        # 3. Ordenar y limitar resultados
        # Primero los que coinciden en ambos criterios (si hubiera, pero aquí ya están separados)
        # Podemos limitar a 10 resultados para no sobrecargar
        similar_users = similar_users[:10]
        
        return jsonify({
            "message": f"Encontrados {len(similar_users)} usuarios similares",
            "similar_users": similar_users,
            "current_user": {
                "hobby": current_hobby,
                "nationality": current_nationality
            }
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@similar_users_routes.route("/api/get_all_users", methods=["GET"])
@cross_origin()
def get_all_users():
    """Endpoint para obtener todos los usuarios (solo datos públicos)"""
    try:
        result = supabase.table("users").select("email, profile_name, nationality, hobby").execute()
        
        # Filtrar usuarios que tienen al menos un dato de perfil
        users_with_profile = [
            user for user in result.data 
            if user.get("profile_name") or user.get("nationality") or user.get("hobby")
        ]
        
        return jsonify({
            "message": "Usuarios obtenidos exitosamente",
            "users": users_with_profile,
            "count": len(users_with_profile)
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500