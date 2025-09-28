from university import University, DegreeNotFoundException

if __name__ == "__main__":
    degree_input = input("Enter the degree you want to search: ")

    try:
        results = University.search_by_degree(degree_input)
        print(f"\nUniversities offering {degree_input}:")
        for uni in results:
            print(f"- {uni.name} (Ranking: {uni.ranking})")
    except DegreeNotFoundException as e:
        print("Error:", e)
