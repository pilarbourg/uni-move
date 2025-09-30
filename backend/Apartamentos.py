import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "database.env"))


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("No se pudo cargar SUPABASE_URL o SUPABASE_KEY del .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def listar_apartamentos():
    result = supabase.table("apartamentos").select("*").execute()
    return result.data

def buscar_precio(presupuesto: float):
    result = (supabase.table("apartamentos")
              .select("id, titulo, barrio, precio")
              .lte("precio", presupuesto)
              .execute())
    return result.data


def buscar_barrio_precio(barrio: str, presupuesto: float):
    result = (
        supabase.table("apartamentos")
        .select("id, titulo, barrio, precio")
        .ilike("barrio", f"%{barrio}%")
        .lte("precio", presupuesto)
        .execute()
    )
    return result.data


def buscar_resultado_vacio(presupuesto: float):
    result = supabase.table("apartamentos").select("*").lte("precio", presupuesto).execute()
    return result.data
