from supabase import create_client, Client

from backend.university_info.university import DegreeNotFoundException

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class UniversityDetailNotFound(Exception):
    pass

class UniversityDetail:
    def __init__(self, id_: int, name: str, ranking: int, public_transport: str, zip_code: int, phone: str):
        self.id = id_
        self.name = name
        self.ranking = ranking
        self.public_transport = public_transport
        self.zip_code = zip_code
        self.phone = phone

    def __repr__(self):
        return (
            f"{self.name} (Ranking: {self.ranking})\n"
            f"  - Public Transport: {self.public_transport}\n"
            f"  - Zip Code: {self.zip_code}\n"
            f"  - Phone: {self.phone}\n"
        )

    @staticmethod
    def get_all_ordered():
        response = (
            supabase.table("universities")
            .select("id, name, ranking, publicTransport, zipCode, phoneNumber")
            .execute()
        )

        data = response.data or []

        if not data:
            raise UniversityDetailNotFound("No universities found in the database.")

        universities = [
            UniversityDetail(
                row["id"],
                row["name"],
                row.get("ranking"),
                row.get("publicTransport"),
                row.get("zipCode"),
                row.get("phoneNumber"),
            )
            for row in data
        ]

        return sorted(
            [u for u in universities if u.ranking is not None],
            key=lambda u: u.ranking,
            reverse=True
        )

    @staticmethod
    def search_by_degree(degree_to_search: str):
        response = (
            supabase.table("universities")
            .select(
                "id, name, ranking, publicTransport, zipCode, phoneNumber, university_degrees(degree_id, degrees(name))")
            .execute()
        )

        data = response.data or []

        results = []
        for row in data:
            if "university_degrees" in row:
                for ud in row["university_degrees"]:
                    if ud["degrees"]["name"].lower() == degree_to_search.lower():
                        results.append(
                            UniversityDetail(
                                row["id"],
                                row["name"],
                                row.get("ranking"),
                                row.get("publicTransport"),
                                row.get("zipCode"),
                                row.get("phoneNumber"),
                            )
                        )

        if not results:
            raise DegreeNotFoundException(f"No universities were found for the degree: {degree_to_search}")

        return sorted(results, key=lambda u: u.ranking)