class User:
    def __init__(self, first_name, last_name, username, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.role = role

class System:
    def __init__(self):
        self.users = []

    def signup(self):
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        role = input("Enter role (admin/waitstaff): ").strip()
        
        for user in self.users:
            if user.username == username:
                print(f"Username '{username}' already exists. Try again.")
                return
        
        new_user = User(first_name, last_name, username, password, role)
        self.users.append(new_user)
        print(f"Signup successful! User '{username}' created as {role}.\n")

    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Login successful!\nWelcome {user.role.capitalize()}!")
                return
        print("Invalid username or password. Try again.\n")

class RestaurantSystem:
    def __init__(self):
        self.system = System()
    
    def display_menu(self):
        while True:
            print("***** Restaurant Management System *****")
            print("1. Signup")
            print("2. Login")
            print("3. Exit")
            choice = input("Select an option: ").strip()
            
            if choice == '1':
                self.system.signup()
            elif choice == '2':
                self.system.login()
            elif choice == '3':
                print("Exit.")
                break
            else:
                print("Invalid choice.")

restaurant_system = RestaurantSystem()
restaurant_system.display_menu()