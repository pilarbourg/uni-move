from backend.university_info.university import University, DegreeNotFoundException
from backend.university_info.university_details import UniversityDetail

#       Requisito 1
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

#      REQUISITO 2
# Comprueba que existe el método para obtener detalles de universidades
def test_detail_method_exists():
    assert hasattr(UniversityDetail, "get_all_ordered")

# Comprueba que se devuelven universidades con info completa
def test_university_detail_fields():
    results = UniversityDetail.get_all_ordered()
    first = results[0]
    assert isinstance(first, UniversityDetail)
    assert first.name is not None
    assert hasattr(first, "phone")
    assert hasattr(first, "zip_code")

# Comprueba que el __repr__ contiene la información esperada
def test_university_detail_repr_format():
    results = UniversityDetail.get_all_ordered()
    text = str(results[0])
    assert "Ranking" in text
    assert "Phone" in text or "Zip" in text

if __name__ == "__main__":
    test_method_exists()
    test_degree_not_found()
    test_degree_found_returns_universities()
    test_results_sorted_by_ranking()
    test_detail_method_exists()
    test_university_detail_fields()
    test_university_detail_repr_format()
    print("All tests passed")