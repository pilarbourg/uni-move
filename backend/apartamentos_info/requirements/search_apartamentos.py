from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ApartmentNotFoundException(Exception):
    pass


class Apartment:
    def __init__(self, id: int, titulo: str, barrio: str, precio: float, disponible: int, amueblado: int):
        self.id = id
        self.titulo = titulo
        self.barrio = barrio
        self.precio = precio
        self.disponible = disponible
        self.amueblado = amueblado

    def __repr__(self):
        return f"{self.titulo} ({self.barrio}) - {self.precio}€"


class ApartmentSearcher:

    @staticmethod
    def get_all():
        response = supabase.table("apartamentos").select("id, titulo, barrio, precio, disponible, amueblado").execute()
        data = response.data or []

        if not data:
            raise ApartmentNotFoundException("No apartments found")

        results = [Apartment(a["id"], a["titulo"], a.get("barrio"), a.get("precio"), a.get("disponible"), a.get("amueblado"))
                   for a in data]

        return results

    @staticmethod
    def search_by_budget(budget: float):
        response = (
            supabase.table("apartamentos")
            .select("id, titulo, barrio, precio, disponible, amueblado")
            .lte("precio", budget)
            .execute()
        )
        data = response.data or []

        if not data:
            raise ApartmentNotFoundException(f"No apartments found under {budget}€")

        results = [Apartment(a["id"], a["titulo"], a.get("barrio"), a.get("precio"), a.get("disponible"), a.get("amueblado"))
                   for a in data]

        return results

    @staticmethod
    def search_by_neighborhood(neighborhood: str):
        response = (
            supabase.table("apartamentos")
            .select("id, titulo, barrio, precio, disponible, amueblado")
            .ilike("barrio", f"%{neighborhood}%")
            .execute()
        )
        data = response.data or []

        if not data:
            raise ApartmentNotFoundException(f"No apartments found in neighborhood {neighborhood}")

        results = [Apartment(a["id"], a["titulo"], a.get("barrio"), a.get("precio"), a.get("disponible"), a.get("amueblado"))
                   for a in data]

        return results
