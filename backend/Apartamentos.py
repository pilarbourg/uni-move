from supabase import create_client, Client

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "TU_API_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def listar_apartamentos():
    result = supabase.table("Apartamentos").select("*") .execute()
    return result.data

def buscar_precio(presupuesto: float):
    result = supabase.table("Apartamentos").select("titulo, precio").lte("precio", presupuesto).execute()
    return result.data

def buscar_barrio_precio(barrio: str, presupuesto: float):
    result = (
        supabase.table("Apartamentos")
        .select("titulo, precio, barrio")
        .eq("barrio", barrio)
        .lte("precio", presupuesto)
        .execute()
    )
    return result.data

def buscar_resultado_vacio(presupuesto: float):
    result = supabase.table("Apartamentos").select("*").lte("precio", presupuesto).execute()
    return result.data