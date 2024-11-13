from src.utility.messages import Messages

class AdminDashboard:
    def __init__(self, system, menu):
        self.system = system
        self.menu = menu

    def admin_actions(self):
        while True:
            Messages.admin_menu()
            choice = input(Messages.select_option()).strip()

            if choice == '1':
                self.system.manage_users()
            elif choice == '2':
                self.menu.manage_menu()
            elif choice == '3':
                Messages.logging_out()
                break
            else:
                Messages.invalid_choice()
