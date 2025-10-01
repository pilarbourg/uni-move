from supabase import create_client, Client

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