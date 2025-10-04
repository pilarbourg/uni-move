from backend.university_info.university_details import UniversityDetail, DegreeNotFoundException

if __name__ == "__main__":
    print("=== Search for universities by degree ===")
    degree = input("Enter the degree you want to search for: ")

    try:
        results = UniversityDetail.search_by_degree(degree)

        print(f"Universities that offer '{degree}':\n")
        for uni in results:
            print(uni)

    except DegreeNotFoundException as e:
        print("Error:", e)
