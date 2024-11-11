from src.utility.messages import Messages


class BillDashboard:
    def __init__(self, bill_feature):
        self.bill_feature = bill_feature

    def manage_bills(self):
        while True:
            Messages.billing_management_menu()

            choice = input(Messages.enter_choice())

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
                Messages.returning_to_dashboard()
                break
            else:
                Messages.invalid_choice()

    def prompt_return_to_dashboard(self):
        while True:
            Messages.prompt_return()
            user_input = input(Messages.enter_choice()).strip().lower()
            if user_input == 'b':
                break
            else:
                Messages.invalid_input_b()
