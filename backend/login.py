class User:
    def __init__(self,email,password):
        self.email = email
        self.password = password

class Login:
    registered_users:list[User]=[User("dx4658@gmail.com","1234")]

    def user_register(self,email,password):
        user_register = User(email,password)
        if user_register.email in self.registered_users:
            raise ValueError("User is already registered")
        self.registered_users.append(user_register)

    def user_login(self,email,password):
        for user in self.registered_users:
            if email == user.email:
                if password == user.password:
                    return True
                else:
                    raise ValueError("Wrong password")
        raise ValueError("User not registered")

    def __str__(self):
        string=""
        string+="--------------"
        string+="\nUNIMOVE\n"
        string+="--------------"
        return string

if __name__=="__main__":
    login = Login()
    print(login)
    choice = input("\nREGISTER OR LOGIN\n")
    if choice == "REGISTER":
        user_register_email = input("\nEnter your email:\n")
        user_register_password = input("\nEnter your password:\n")
        login.user_register(user_register_email,user_register_password)
        print("\nAccount created successfully!\n")
    if choice == "LOGIN":
        user_login_email = input("\nEnter your email:\n")
        user_login_password = input("\nEnter your password:\n")
        login.user_login(user_login_email,user_login_password)
        print(f"\nWelcome {user_login_email}!\n")