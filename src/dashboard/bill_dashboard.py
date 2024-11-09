class BillDashboard:
    def __init__(self, bill_feature):
        self.bill_feature = bill_feature

    def manage_bills(self):
        while True:
            print("\n--- Billing Management ---")
            print("1. Create Bill")
            print("2. Update Bill")
            print("3. Delete Bill")
            print("4. Search Bill by Table Number")
            print("5. View All Bills")
            print("6. Go Back to Dashboard")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.bill_feature.bill_create()
            elif choice == '2':
                self.bill_feature.update()
            elif choice == '3':
                self.bill_feature.delete_bill()
            elif choice == '4':
                self.bill_feature.search_bill_by_table()
                self.prompt_return_to_dashboard()
            elif choice == '5':
                self.bill_feature.search_all_bills()
                self.prompt_return_to_dashboard()
            elif choice == '6':
                print("Returning to the main dashboard.")
                break
            else:
                print("Invalid choice. Please try again.")

    def prompt_return_to_dashboard(self):
        while True:
            print("\nEnter 'b' to go back to the main dashboard.")
            user_input = input("Enter choice: ").strip().lower()
            if user_input == 'b':
                break
            else:
                print("Invalid input. Please enter 'b' to go back.")
