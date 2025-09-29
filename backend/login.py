import os

from dotenv import load_dotenv
from supabase import create_client, Client
import bcrypt

SUPABASE_URL="https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

usuarios = supabase.table("users").select("*").execute()

class User:
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

class Login:
    def user_register(self,name,email,password):
        user_register = User(name,email,password)
        if user_register.email in usuarios:
            raise ValueError("User is already registered")
        supabase.table("users").insert({"name": user_register.name,"email": user_register.email,"password": user_register.password}).execute()

    def user_login(self,email,password):
        emails = supabase.table("users").select("*").eq("email", email).execute().data
        if not emails:
            raise ValueError("User is not registered")
        user = emails[0]
        stored_hash = user["password_hash"].encode["utf-8"]
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True
        else:
            raise ValueError("Wrong password")

    def __str__(self):
        string=""
        string+="--------------"
        string+="\nUNIMOVE\n"
        string+="--------------"
        return string

if __name__=="__main__":
    login = Login()
    print(login)
    for user in usuarios:
        print(user.email)
    choice = input("\nREGISTER OR LOGIN\n")
    if choice == "REGISTER":
        user_register_name = input("\nEnter your username:\n")
        user_register_email = input("\nEnter your email:\n")
        user_register_password = input("\nEnter your password:\n")
        login.user_register(user_register_name,user_register_email,user_register_password)
        print("\nAccount created successfully!\n")
    if choice == "LOGIN":
        user_login_email = input("\nEnter your email:\n")
        user_login_password = input("\nEnter your password:\n")
        for user in usuarios:
            if user.email==user_login_email and user.password==user_login_password:
                user_login_name=user.name
                login.user_login(user_login_email, user_login_password)
                print(f"\nWelcome {user_login_name}!\n")