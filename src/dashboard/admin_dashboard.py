from src.dashboard.order_dashboard import OrderDashboard
from src.utility.messages import messages
from src.utility.color import bcolors
from src.dashboard.menu_dashboard import MenuDashboard
from src.utility.reports import Reports

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
            print("4. View Reports")
            print("5. Logout")
            
            choice = input(bcolors.colorize("Select an option: ", bcolors.TEAL)).strip()

            if choice == '1':
                self.system.manage_users()
            elif choice == '2':
                self.menu_dashboard.manage_menu('admin')
            elif choice == '3':
                self.order_dashboard.manage_orders(user_role='admin')
            elif choice == '4':
                self.view_reports()
            elif choice == '5':
                print(messages.log_out)
                break
            else:
                print(bcolors.colorize(messages.invalid_choice, bcolors.RED))
    
    def view_reports(self):
        while True:
            print("\n --- Reports ---")
            print("1. Weekly Sales Report")
            print("2. Today's Sales Report")
            print(messages.prompt_return)

            user_input = input("Enter your choice: ").strip().lower()

            if user_input == '1':
                self.show_weekly_report()
                self.prompt_return_to_dashboard()
            elif user_input == '2':
                self.show_daily_report()
                self.prompt_return_to_dashboard()
            elif user_input == 'b':
                print("Returning to Admin Menu...")
                return
            else:
                print(messages.invalid_input)
                self.view_reports()
    
    def show_weekly_report(self):
        Reports.generate_sales_report()
        try:
            with open("src/database/sales_report.txt", 'r') as file:
                full_report = file.read()
            
            print("\n" + "=" * 60)
            print(f"{'Weekly Sales Report (Last 7 Days)':^60}")
            print("=" * 60)

            start_idx = full_report.find("Weekly Sales Report")
            end_idx = full_report.find("Today's Sales Report")
            weekly_report = full_report[start_idx:end_idx].strip()

            print(weekly_report)
        except FileNotFoundError:
            print("Weekly sales report file not found.")
        except Exception as e:
            print(f"An error occurred while reading the report: {e}")
            
    def show_daily_report(self):
        Reports.generate_sales_report()
        try:
            with open("src/database/sales_report.txt", 'r') as file:
                full_report = file.read()
            
            print("\n" + "=" * 60)
            print(f"{'Today\'s Sales Report':^60}")
            print("=" * 60)

            start_idx = full_report.find("Today's Sales Report")
            daily_report = full_report[start_idx:].strip()

            print(daily_report)
        except FileNotFoundError:
            print("Daily sales report file not found.")
        except Exception as e:
            print(f"An error occurred while reading the report: {e}")
            
    def prompt_return_to_dashboard(self):
        while True:
            print(messages.prompt_return)
            user_input = input("Enter your choice: ").strip().lower()
            if user_input == 'b':
                break
            else:
                print(messages.invalid_input)
