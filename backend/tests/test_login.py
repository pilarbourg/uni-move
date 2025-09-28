import pytest
from backend.login import Login

def test_user_register_new_user(login_instance=Login()):
    login_instance.user_register("sofia","sofia@gmail.com","1234")
    assert any(user.email == "sofia@gmail.com" for user in databasetest)

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