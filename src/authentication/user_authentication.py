import json
import os
from src.utility.validations import admin_check, is_username_taken
from src.dashboard.admin_dashboard import AdminDashboard
from src.dashboard.staff_dashboard import StaffDashboard
from src.menu.menu import Menu
from src.orders.order_feature import OrderFeature
from src.manage_bill.bill_feature import BillFeature
from src.booking.table_booking import TableBookingSystem
from src.dashboard.bill_dashboard import BillDashboard

USER_FILE_PATH = "src/database/user.json"

class System:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(USER_FILE_PATH):
            with open(USER_FILE_PATH, 'r') as file:
                return json.load(file)
        return []

    def save_users(self):
        with open(USER_FILE_PATH, 'w') as file:
            json.dump(self.users, file, indent=4)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                print(f"Welcome back, {username}!")
                return user
        print("Invalid credentials.")
        return None

    def signup(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if is_username_taken(self.users, username):
            print("Username already exists. Try a different one.")

        role = 'admin' if not admin_check(self.users) else 'staff'
        new_user = {
            'first_name': input("Enter first name: "),
            'last_name': input("Enter last name: "),
            'username': username,
            'password': password,
            'role': role
        }
        self.users.append(new_user)
        self.save_users()
        print(f"User {username} signed up successfully as {role}.")

    def manage_users(self):
        while True:
            print("\n--- Manage Users ---")
            print("1. View All Users")
            print("2. Add New User")
            print("3. Delete User")
            print("4. Back to Admin Menu")
            choice = input("Choose an option: ").strip()

            if choice == '1':
                self.view_users()
            elif choice == '2':
                self.signup()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_users(self):
        if self.users:
            print("\nRegistered Users:")
            for user in self.users:
                print(f"Username: {user['username']}, Role: {user['role']}")
        else:
            print("No registered users found.")

    def delete_user(self):
        username = input("Enter the username of the user to delete: ").strip()
        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                self.save_users()
                print(f"User '{username}' deleted successfully.")
        print(f"User '{username}' not found.")

class RestaurantSystem:
    def __init__(self):
        self.system = System()
        self.table_booking = TableBookingSystem()
        self.order_feature = OrderFeature()
        self.bill_feature = BillFeature()
        self.bill_dashboard = BillDashboard(self.bill_feature)
        self.menu = Menu()

    def display_menu(self):
        user = None
        while True:
            print("\n***** Welcome to the System *****")
            print("1. Login")
            print("2. Sign up")
            print("3. Exit")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                user = self.system.login()
                if user:
                    break
            elif choice == '2':
                self.system.signup()
            elif choice == '3':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

        if user:
            if user['role'] == 'admin':
                admin_dashboard = AdminDashboard(self.system, self.menu)
                admin_dashboard.admin_actions()
            elif user['role'] == 'staff':
                staff_dashboard = StaffDashboard(self.menu, self.table_booking, self.order_feature, self.bill_dashboard)
                staff_dashboard.staff_actions()