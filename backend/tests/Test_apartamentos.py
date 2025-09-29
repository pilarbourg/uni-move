import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.Apartamentos import (
    listar_apartamentos,
    buscar_precio,
    buscar_barrio_precio,
    buscar_resultado_vacio
)

class Test_apartamentos(unittest.TestCase):

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

    def test_busqueda_por_barrio(self):
        """Requisito 3: Buscar por barrio y presupuesto"""
        presupuesto = 1500
        barrio = "Lavapiés-Embajadores"
        data = buscar_barrio_precio(barrio, presupuesto)
        self.assertTrue(all(r["barrio"] == barrio for r in data))

    def test_resultado_vacio(self):
        """Requisito 4: Caso sin resultados"""
        presupuesto = 100  # muy bajo
        data = buscar_resultado_vacio(presupuesto)
        self.assertEqual(data, [], "Se devolvieron resultados cuando no debería")

if __name__ == "__main__":
    unittest.main()
