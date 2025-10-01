import pytest
from backend.login import Login
from supabase import create_client, Client

SUPABASE_URL="https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

usuarios = supabase.table("users").select("*").execute()

def test_user_register_new_user(login_instance=Login()):
    login_instance.user_register("sofia","sofia@gmail.com","1234")
    assert any(usuarios.data[user]["email"] == "sofia@gmail.com" for user in range(len(usuarios.data)))
    
def test_user_register_existing_user(login_instance=Login()):
    with pytest.raises(ValueError) as error:
        login_instance.user_register("david", "dx4658@gmail.com", "1234")
    assert str(error.value) == "User is already registered"

def test_user_login_success(login_instance=Login()):
    assert login_instance.user_login("dx4658@gmail.com", "1234") == True

def test_user_login_wrong_password(login_instance=Login()):
    with pytest.raises(ValueError) as error:
        login_instance.user_login("dx4658@gmail.com", "wrong")
    assert str(error.value) == "Wrong password"

def test_user_login_nonexistent_user(login_instance=Login()):
    with pytest.raises(ValueError) as error:
        login_instance.user_login("pepe@gmail.com", "1234")
    assert str(error.value) == "User not registered"