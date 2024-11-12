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
from src.utility.messages import Messages

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
        username = input("Enter username: ").strip().lower()
        password = input("Enter password: ").strip().lower()
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                Messages.welcome_back(username)
                return user
        Messages.invalid_credentials()
        return None

    def signup(self):
        username = input("Enter username: ").strip().lower()
        password = input("Enter password: ").strip().lower()
        if is_username_taken(self.users, username):
            Messages.username_exists()
            return

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
        Messages.signup_success(username, role)

    def manage_users(self):
        while True:
            Messages.manage_users_menu()
            choice = input(Messages.choose_option()).strip()

            if choice == '1':
                self.view_users()
            elif choice == '2':
                self.signup()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                break
            else:
                Messages.invalid_choice()

    def view_users(self):
        if self.users:
            Messages.registered_users()
            for user in self.users:
                Messages.user_details(user['username'], user['role'])
        else:
            Messages.no_users()

    def delete_user(self):
        username = input(Messages.enter_username_to_delete()).strip().lower()
        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                self.save_users()
                Messages.user_deleted(username)
                return
        Messages.user_not_found(username)

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
            Messages.welcome_system()
            choice = input(Messages.choose_option()).strip()
            if choice == '1':
                user = self.system.login()
                if user:
                    break
            elif choice == '2':
                self.system.signup()
            elif choice == '3':
                Messages.exit_system()
                break
            else:
                Messages.invalid_choice()

        if user:
            if user['role'] == 'admin':
                admin_dashboard = AdminDashboard(self.system, self.menu)
                admin_dashboard.admin_actions()
            elif user['role'] == 'staff':
                staff_dashboard = StaffDashboard(self.menu, self.table_booking, self.order_feature, self.bill_dashboard)
                staff_dashboard.staff_actions()