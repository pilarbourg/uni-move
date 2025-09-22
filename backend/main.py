from university import University
from university_searcher import UniversitySearcher, DegreeNotFoundException

def main():
    # Example university list
    universities = [
        University("Complutense University", "Computer Science", 2),
        University("Autonomous University", "Medicine", 1),
        University("Polytechnic University", "Computer Science", 3),
        University("University of Alcalá", "Law", 5),
        University("Carlos III University", "Computer Science", 4)
    ]

    degree_to_search = input("Enter the degree you want to search: ")

    #   Si no hay error te muestra la lista de Universidades

    try:
        results = UniversitySearcher.search_by_degree(universities, degree_to_search)

        print(f"\nUniversities offering {degree_to_search}:")
        for u in results:
            print(f"- {u.name} (Ranking: {u.ranking})")

    except DegreeNotFoundException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
