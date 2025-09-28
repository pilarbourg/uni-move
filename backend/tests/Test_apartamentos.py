import unittest
from supabase import create_client, Client

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "TU_API_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Test_apartamentos(unittest.TestCase):

    def test_listar_apartamentos(self):
        resultado = supabase.table("Apartamentos").select("titulo,precio").execute()
        data = resultado.data
        self.assertGreater(len(data), 0, "No existen apartamentos")
        for row in data:
            self.assertIsNotNone(row["titulo"])
            self.assertGreater(row["precio"], 0)

    def test_busqueda_precio(self):
        presupuesto = 1000
        resultado = supabase.table("Apartamentos").select("titulo,precio").lte("precio", presupuesto).execute()
        data = resultado.data
        self.assertGreater(len(data), 0, "No existen apartamentos en ese presupuesto")
        for row in data:
            self.assertLessEqual(row["precio"], presupuesto)

    def test_busqueda_por_barrio(self):
        presupuesto = 1500
        barrio = "Lavapiés-Embajadores"
        resultado = supabase.table("Apartamentos").select("titulo,precio,barrio").eq("barrio", barrio).lte("precio", presupuesto).execute()
        data = resultado.data
        self.assertTrue(all(r["barrio"] == barrio for r in data))

    def test_resultado_vacio(self):
        presupuesto = 100
        resultado = supabase.table("Apartamentos").select("*").lte("precio", presupuesto).execute()
        data = resultado.data
        self.assertEqual(data, [], "Se devolvieron resultados cuando no debería")

if __name__ == "__main__":
    unittest.main()
