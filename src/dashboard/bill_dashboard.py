from src.utility.messages import messages
from src.utility.color import bcolors

class BillDashboard:
    def __init__(self, bill_feature):
        self.bill_feature = bill_feature

    def manage_bills(self):
        while True:
            print(bcolors.colorize("\n--- Billing Management ---", bcolors.LIGHT_GREEN))
            print("1. Create Bill")
            print("2. Update Bill")
            print("3. Delete Bill")
            print("4. Search Bill")
            print("5. View All Bills")
            print("6. Go Back to Dashboard")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.bill_feature.bill_create()
            elif choice == '2':
                self.bill_feature.update()
            elif choice == '3':
                self.bill_feature.delete_bill()
            elif choice == '4':
                self.bill_feature.search_bill_by_id()
                self.prompt_return_to_dashboard()
            elif choice == '5':
                self.bill_feature.search_all_bills()
                self.prompt_return_to_dashboard()
            elif choice == '6':
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
                print(bcolors.colorize(messages.invalid_input, bcolors.RED))
