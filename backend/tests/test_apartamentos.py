import unittest
from unittest.mock import patch, MagicMock
import sys, os

# Permitir import desde backend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.apartamentos_info.apartamentos import (
    listar_apartamentos,
    buscar_precio,
    buscar_barrio_precio,
    buscar_resultado_vacio,
)


class TestApartamentos(unittest.TestCase):

    # --- 1. LISTAR ---
    @patch("backend.apartamentos_info.apartamentos.supabase")
    def test_listar_apartamentos(self, mock_supabase):
        # Simula .execute() devolviendo un objeto con .data
        mock_execute = MagicMock()
        mock_execute.data = [
            {"titulo": "Piso bonito", "precio": 950, "barrio": "Moncloa"}
        ]
        mock_supabase.table.return_value.select.return_value.execute.return_value = mock_execute

        data = listar_apartamentos()

        self.assertIsInstance(data, list, "Debe devolver una lista")
        self.assertIn("titulo", data[0])
        self.assertIn("precio", data[0])

    # --- 2. PRECIO ---
    @patch("backend.apartamentos_info.apartamentos.supabase")
    def test_busqueda_precio(self, mock_supabase):
        mock_execute = MagicMock()
        mock_execute.data = [
            {"titulo": "Piso barato", "precio": 800},
            {"titulo": "Piso justo", "precio": 1000},
        ]
        mock_supabase.table.return_value.select.return_value.lte.return_value.execute.return_value = mock_execute

        presupuesto = 1000
        data = buscar_precio(presupuesto)
        self.assertIsInstance(data, list)
        for row in data:
            self.assertLessEqual(row["precio"], presupuesto)

    # --- 3. BARRIO + PRECIO ---
    @patch("backend.apartamentos_info.apartamentos.supabase")
    def test_buscar_barrio_precio(self, mock_supabase):
        mock_execute = MagicMock()
        mock_execute.data = [
            {"barrio": "Moncloa", "precio": 1200},
            {"barrio": "Moncloa Centro", "precio": 1800},
        ]
        mock_supabase.table.return_value.select.return_value.ilike.return_value.lte.return_value.execute.return_value = mock_execute

        data = buscar_barrio_precio("Moncloa", 2000)
        for apt in data:
            self.assertIn("moncloa", apt["barrio"].lower())
            self.assertLessEqual(float(apt["precio"]), 2000)

    # --- 4. RESULTADO VACÍO ---
    @patch("backend.apartamentos_info.apartamentos.supabase")
    def test_resultado_vacio(self, mock_supabase):
        mock_execute = MagicMock()
        mock_execute.data = []  # No resultados
        mock_supabase.table.return_value.select.return_value.lte.return_value.execute.return_value = mock_execute

        presupuesto = 50
        data = buscar_resultado_vacio(presupuesto)
        self.assertEqual(len(data), 0, "Se devolvieron resultados cuando no debería")


if __name__ == "__main__":
    unittest.main()
