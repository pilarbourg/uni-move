from university import University, DegreeNotFoundException


# Comprueba que la clase University tiene el método
def test_method_exists():
    assert hasattr(University, "search_by_degree")

# Comprueba que si buscamos un grado que no existe, se lanza la excepción
def test_degree_not_found():
    try:
        University.search_by_degree("GradoInventado")
        assert False, "Debió lanzar DegreeNotFoundException"
    except DegreeNotFoundException:
        pass

# Comprueba que si el grado existe en la BBDD, devuelve una lista con universidades
def test_degree_found_returns_universities():
    results = University.search_by_degree("Economics")  # asegúrate de que exista en tu BBDD
    assert len(results) > 0
    assert isinstance(results[0], University)

# Comprueba que los resultados devueltos están ordenados por ranking de menor a mayor
def test_results_sorted_by_ranking():
    results = University.search_by_degree("Economics")  # asegúrate de que exista en tu BBDD
    rankings = [u.ranking for u in results]
    assert rankings == sorted(rankings)


if __name__ == "__main__":
    test_method_exists()
    test_degree_not_found()
    test_degree_found_returns_universities()
    test_results_sorted_by_ranking()
    print("✅ Todos los tests pasaron correctamente")
