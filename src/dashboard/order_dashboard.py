from src.orders.order_feature import OrderFeature
from src.utility.messages import messages

class OrderDashboard:
    def __init__(self):
        self.order_feature = OrderFeature()

    def manage_orders(self, user_role='staff'):
        while True:
            print("\n--- Order Management ---")
            print("1. Add Order")
            print("2. Update Order")
            print("3. Cancel Order")
            print("4. Search Order")
            print("5. View All Orders")
            print("6. Go Back to Dashboard")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.order_feature.order()
            elif choice == '2':
                self.order_feature.update_item()
            elif choice == '3':
                if user_role == 'admin':
                    self.order_feature.cancel_item()
                else:
                    print("Permission Denied: Only admins can cancel orders.")
            elif choice == '4':
                self.order_feature.search_order()
                self.prompt_return_to_dashboard()
            elif choice == '5':
                self.order_feature.search_all_orders()
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
                print(messages.invalid_input)
