from src.dashboard.bill_dashboard import BillDashboard

class StaffDashboard:
    def __init__(self, menu_dashboard, booking_dashboard, order_dashboard, bill_dashboard: BillDashboard):
        self.menu_dashboard = menu_dashboard
        self.booking_dashboard = booking_dashboard
        self.order_dashboard = order_dashboard
        self.bill_dashboard = bill_dashboard

    def staff_actions(self):
        while True:
            print("\n***** Staff Menu *****")
            print("1. Manage Menu")
            print("2. Manage Table Bookings")
            print("3. Manage Orders")
            print("4. Manage Bills")
            print("5. Logout")

            choice = input("Select an option: ")
            if choice == '1':
                self.menu_dashboard.manage_menu()
            elif choice == '2':
                self.booking_dashboard.manage_bookings()
            elif choice == '3':
                self.order_dashboard.manage_orders()
            elif choice == '4':
                self.bill_dashboard.manage_bills()
            elif choice == '5':
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please try again.")
