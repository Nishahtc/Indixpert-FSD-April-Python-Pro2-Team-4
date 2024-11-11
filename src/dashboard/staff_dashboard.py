from src.dashboard.bill_dashboard import BillDashboard
from src.utility.messages import Messages

class StaffDashboard:
    def __init__(self, menu_dashboard, booking_dashboard, order_dashboard, bill_dashboard: BillDashboard):
        self.menu_dashboard = menu_dashboard
        self.booking_dashboard = booking_dashboard
        self.order_dashboard = order_dashboard
        self.bill_dashboard = bill_dashboard

    def staff_actions(self):
        while True:
            Messages.staff_menu()

            choice = input(Messages.select_option())
            if choice == '1':
                self.menu_dashboard.manage_menu()
            elif choice == '2':
                self.booking_dashboard.manage_bookings()
            elif choice == '3':
                self.order_dashboard.manage_orders()
            elif choice == '4':
                self.bill_dashboard.manage_bills()
            elif choice == '5':
                Messages.logging_out()
                break
            else:
                Messages.invalid_choice()
