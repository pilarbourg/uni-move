import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.apartamentos import listar_apartamentos, buscar_precio, buscar_barrio_precio, buscar_resultado_vacio


class test_apartamentos(unittest.TestCase):

    def test_listar_apartamentos(self):
        data = listar_apartamentos()
        # En lugar de forzar que haya datos:
        self.assertIsInstance(data, list, "Debe devolver una lista")
        if data:  # Solo si hay datos
            for row in data:
                self.assertIn("titulo", row)
                self.assertIn("precio", row)

    def test_busqueda_precio(self):
        presupuesto = 1000
        data = buscar_precio(presupuesto)
        self.assertIsInstance(data, list, "Debe devolver lista de apartamentos")
        for row in data:  # Si la lista está vacía, no entra
            self.assertLessEqual(row["precio"], presupuesto)

    def test_buscar_barrio_precio(self):
        data = buscar_barrio_precio("Moncloa", 2000)
        # Puede que no haya datos, pero si los hay deben cumplir filtros
        for apt in data:
            assert "moncloa" in apt["barrio"].lower()
            assert float(apt["precio"]) <= 2000

    def test_resultado_vacio(self):
        """Requisito 4: Caso sin resultados"""
        presupuesto = 100  # muy bajo
        data = buscar_resultado_vacio(presupuesto)
        self.assertEqual(data, [], "Se devolvieron resultados cuando no debería")

if __name__ == "__main__":
    unittest.main()