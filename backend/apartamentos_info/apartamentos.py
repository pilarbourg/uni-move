import os
from supabase import create_client, Client
#from dotenv import load_dotenv

#load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "database.env"))

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def listar_apartamentos():
    result = (
        supabase.table("apartamentos")
        .select("id, titulo, barrio, precio, latitude, longitude, tamano_m2")
        .execute()
    )
    return result.data

def buscar_precio(presupuesto: float):
    result = (
        supabase.table("apartamentos")
        .select("id, titulo, barrio, precio, latitude, longitude, tamano_m2")
        .lte("precio", presupuesto)
        .execute()
    )
    return result.data


def buscar_barrio_precio(barrio: str, presupuesto: float):
    result = (
        supabase.table("apartamentos")
        .select("id, titulo, barrio, precio, latitude, longitude, tamano_m2")
        .ilike("barrio", f"%{barrio}%")
        .lte("precio", presupuesto)
        .execute()
    )
    return result.data


def buscar_resultado_vacio(presupuesto: float):
    result = supabase.table("apartamentos").select("*").lte("precio", presupuesto).execute()
    return result.data

