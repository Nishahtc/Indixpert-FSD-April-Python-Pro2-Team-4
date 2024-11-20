from src.menu.menu import Menu
from src.utility.messages import messages

class MenuDashboard:
    def __init__(self):
        self.menu = Menu()

    def manage_menu(self, user_role):
        while True:
            if user_role == 'staff':
                self.menu.view_menu()
                self.prompt_return_to_dashboard()
                break

            print("\n--- Menu Management ---")
            print("1. View Menu")
            print("2. Add Menu Item")
            print("3. Remove Menu Item")
            print("4. Go Back to Dashboard")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                self.menu.view_menu()
                self.prompt_return_to_dashboard()
            elif choice == '2':
                self.menu.handle_add_item()
            elif choice == '3':
                self.menu.handle_remove_item()
            elif choice == "4":
                print(messages.returning_dashboard)
                break
            else:
                print(messages.invalid_choice)

    def prompt_return_to_dashboard(self):
        while True:
            print(messages.prompt_return)
            user_input = input("Enter your choice: ").strip().lower()
            if user_input == 'b':
                break
            else:
                print(messages.invalid_input)
