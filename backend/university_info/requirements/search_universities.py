from supabase import create_client, Client

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class DegreeNotFoundException(Exception):
    pass

class University:
    def __init__(self, id_: int, name: str, ranking: int):
        self.id = id_
        self.name = name
        self.ranking = ranking

    def __repr__(self):
        return f"{self.name} (Ranking: {self.ranking})"

    @staticmethod
    def search_by_degree(degree_to_search: str):

        response = (
            supabase.table("universities")
            .select("id, name, ranking, university_degrees(degree_id, degrees(name))")
            .execute()
        )

        data = response.data or []

        results = []
        for row in data:
            if "university_degrees" in row:
                for ud in row["university_degrees"]:
                    if ud["degrees"]["name"].lower() == degree_to_search.lower():
                        results.append(University(row["id"], row["name"], row["ranking"]))

        if not results:
            raise DegreeNotFoundException(f"No universities found for the degree: {degree_to_search}")

        return sorted(results, key=lambda u: u.ranking)
