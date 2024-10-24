import json
import os

DATABASE_FOLDER = "src/database"
USERS_FILE_PATH = os.path.join(DATABASE_FOLDER, "users.json")

class User:
    def __init__(self, first_name, last_name, username, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(user_data):
        return User(
            user_data['first_name'],
            user_data['last_name'],
            user_data['username'],
            user_data['password'],
            user_data['role']
        )

class System:
    def __init__(self, users_file=USERS_FILE_PATH):
        if not os.path.exists(DATABASE_FOLDER):
            os.makedirs(DATABASE_FOLDER)

        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                try:
                    users_data = json.load(f)
                    return [User.from_dict(user) for user in users_data]
                except json.JSONDecodeError:
                    print("Starting with an empty user list.") #if json error happens.
                    return []
        return []

    def save_users(self):
        with open(self.users_file, 'w') as f:
            users_data = [user.to_dict() for user in self.users]
            json.dump(users_data, f, indent=4)

    def is_admin_present(self):
        for user in self.users:
            if user.role == 'admin':
                return True
        return False

    def signup(self):
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if not self.is_admin_present():
            role = 'admin'
            print("First user registered as Admin.")
        else:
            role = 'staff'

        for user in self.users:
            if user.username == username:
                print(f"Username '{username}' already exists. Try again.")
                return

        new_user = User(first_name, last_name, username, password, role)
        self.users.append(new_user)
        self.save_users()
        print(f"Signup successful! User '{username}' created as {role}.\n")

    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Login successful! Welcome {user.first_name} ({user.role.capitalize()}).\n")
                return user
        print("Invalid username or password. Try again.\n")
        return None

    def admin_tasks(self):
        while True:
            print("\n***** Admin Tasks *****")
            print("1. Add menu item (mockup)")
            print("2. Update menu item (mockup)")
            print("3. Delete menu item (mockup)")
            print("4. View all users (mockup)")
            print("5. Delete a user (mockup)")
            print("6. Logout")
            choice = input("Select an option: ").strip()

            if choice == '6':
                print("Logging out...\n")
                break
            else:
                print(f"Selected admin task {choice}.\n")

    def staff_tasks(self):
        while True:
            print("\n***** Staff Tasks *****")
            print("1. Take customer order (mockup)")
            print("2. Manage table reservations (mockup)")
            print("3. Logout")
            choice = input("Select an option: ").strip()

            if choice == '3':
                print("Logging out...\n")
                break
            else:
                print(f"Selected staff task {choice}.\n")

class RestaurantSystem:
    def __init__(self):
        self.system = System()

    def display_menu(self):
        while True:
            print("\n***** Restaurant Management System *****")
            print("1. Signup")
            print("2. Login")
            print("3. Exit")
            choice = input("Select an option: ").strip()

            if choice == '1':
                self.system.signup()
            elif choice == '2':
                user = self.system.login()
                if user:
                    self.role_based_menu(user)
            elif choice == '3':
                print("Exit.")
                break
            else:
                print("Invalid choice. Please try again.")

    def role_based_menu(self, user):
        if user.role == 'admin':
            self.system.admin_tasks()
        elif user.role == 'staff':
            self.system.staff_tasks()

restaurant_system = RestaurantSystem()
restaurant_system.display_menu()