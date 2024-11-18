import json
import os
from src.utility.validations import is_username_taken, admin_check, validate_email, validate_mobile_number
from src.dashboard.admin_dashboard import AdminDashboard
from src.dashboard.staff_dashboard import StaffDashboard
from src.menu.menu import Menu
from src.orders.order_feature import OrderFeature
from src.manage_bill.bill_feature import BillFeature
from src.booking.table_booking import TableBookingSystem
from src.dashboard.bill_dashboard import BillDashboard
from getpass import getpass
from src.utility.log import log_login, log_logout
from src.utility.messages import messages
from src.utility.color import bcolors

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
        try:
            with open(USER_FILE_PATH, 'w') as file:
                json.dump(self.users, file, indent=4)
        except Exception:
            print(messages.data_save_error)

    def login(self):
        username = input(bcolors.colorize("Enter username: ", bcolors.PINK)).strip().lower()
        password = getpass(bcolors.colorize("Enter password: ", bcolors.PINK)).strip().lower()
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                print(bcolors.colorize(f"Welcome back, {username}!", bcolors.LIGHT_GREEN))
                log_login(username, user['role'])
                return user
        print(bcolors.colorize(messages.invalid_credentials, bcolors.RED))
        return None

    def signup(self):
        username = input("Enter username: ").strip().lower()
        password = getpass("Enter password: ").strip().lower()
        if is_username_taken(self.users, username):
            print(messages.username_exists)
            return
        
        email = input("Enter email: ").strip().lower()
        mobile_number = input("Enter mobile number: ")
        
        if not validate_email(email):
            print(messages.invalid_email)
            return
        
        if not validate_mobile_number(mobile_number):
            print(messages.invalid_mobile_number)
            return

        role = 'admin' if not admin_check(self.users) else 'staff'
        new_user = {
            'first_name': input("Enter first name: "),
            'last_name': input("Enter last name: "),
            'username': username,
            'password': password,
            'email': email,
            'mobile_number': mobile_number,
            'role': role
        }
        self.users.append(new_user)
        self.save_users()
        print(messages.user_signup_success)

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
                print(messages.invalid_choice)

    def view_users(self):
        if self.users:
            print("\nRegistered Users:")
            for user in self.users:
                print(f"Username: {user['username']}, Role: {user['role']}, Email: {user['email']}, Mobile: {user['mobile_number']}")
        else:
            print(messages.no_registered_users)

    def delete_user(self):
        username = input("Enter the username of the user to delete: ").strip().lower()
        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                self.save_users()
                print(messages.user_deleted)
                return
        print(messages.user_not_found)

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
            print(bcolors.colorize("\n***** Welcome to One Bite Restaurant System *****", bcolors.TEAL))
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
                print(messages.exiting_system)
                break
            else:
                print(messages.invalid_choice)

        if user:
            if user['role'] == 'admin':
                admin_dashboard = AdminDashboard(self.system, self.menu)
                admin_dashboard.admin_actions()
                log_logout(user['username'], user['role'])
            elif user['role'] == 'staff':
                staff_dashboard = StaffDashboard(self.menu, self.table_booking, self.order_feature, self.bill_dashboard)
                staff_dashboard.staff_actions()
                log_logout(user['username'], user['role'])
