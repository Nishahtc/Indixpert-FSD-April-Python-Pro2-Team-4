from src.dashboard.order_dashboard import OrderDashboard
from src.utility.messages import messages
from src.utility.color import bcolors
from src.dashboard.menu_dashboard import MenuDashboard

class AdminDashboard:
    def __init__(self, system, menu):
        self.system = system
        self.menu = menu
        self.order_dashboard = OrderDashboard()
        self.menu_dashboard = MenuDashboard()

    def admin_actions(self):
        while True:
            print(bcolors.colorize("\n***** Admin Menu *****", bcolors.PURPLE))
            print("1. Manage Users")
            print("2. Manage Menu")
            print("3. Manage Orders")
            print("4. Logout")
            
            choice = input(bcolors.colorize("Select an option: ", bcolors.TEAL)).strip()

            if choice == '1':
                self.system.manage_users()
            elif choice == '2':
                self.menu_dashboard.manage_menu('admin')
            elif choice == '3':
                self.order_dashboard.manage_orders(user_role='admin')
            elif choice == '4':
                print(messages.log_out)
                break
            else:
                print(bcolors.colorize(messages.invalid_choice, bcolors.RED))
