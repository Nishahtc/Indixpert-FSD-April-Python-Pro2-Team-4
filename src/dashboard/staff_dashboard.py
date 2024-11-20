from src.dashboard.bill_dashboard import BillDashboard
from src.utility.messages import messages
from src.utility.color import bcolors
from src.dashboard.menu_dashboard import MenuDashboard
from src.dashboard.order_dashboard import OrderDashboard

class StaffDashboard:
    def __init__(self, menu_dashboard, booking_dashboard, order_dashboard, bill_dashboard: BillDashboard):
        self.menu_dashboard = menu_dashboard
        self.booking_dashboard = booking_dashboard
        self.order_dashboard = OrderDashboard()
        self.bill_dashboard = bill_dashboard
        self.menu_dashboard = MenuDashboard()

    def staff_actions(self):
        while True:
            print(bcolors.colorize("\n***** Staff Menu *****", bcolors.ORANGE))
            print("1. View Menu")
            print("2. Manage Table Bookings")
            print("3. Manage Orders")
            print("4. Manage Bills")
            print("5. Logout")

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.menu_dashboard.manage_menu('staff')
            elif choice == '2':
                self.booking_dashboard.manage_bookings()
            elif choice == '3':
                self.order_dashboard.manage_orders(user_role='staff')
            elif choice == '4':
                self.bill_dashboard.manage_bills()
            elif choice == '5':
                print(messages.log_out)
                break
            else:
                print(bcolors.colorize(messages.invalid_choice, bcolors.RED))
