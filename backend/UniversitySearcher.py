from typing import List
from university import University

class DegreeNotFoundException(Exception):
    pass

class UniversitySearcher:
    @staticmethod

    # devuelve lisra de universidades encontradas
    def search_by_degree(universities: List[University], degree_to_search: str) -> List[University]:
        results = [u for u in universities if u.degree.lower() == degree_to_search.lower()]  # list comprehension: se queda solo con las q cumplan la condición

        if not results:
            raise DegreeNotFoundException(f"No universities found for the degree: {degree_to_search}")

        # Sort by ranking (descending order)
        results.sort(key=lambda u: u.ranking)
        return results


