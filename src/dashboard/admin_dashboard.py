class AdminDashboard:
    def __init__(self, system, menu):
        self.system = system
        self.menu = menu

    def admin_actions(self):
        while True:
            print("\n***** Admin Menu *****")
            print("1. Manage Users")
            print("2. Manage Menu")
            print("3. Logout")
            choice = input("Select an option: ").strip()

            if choice == '1':
                self.system.manage_users()
            elif choice == '2':
                self.menu.manage_menu()
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
