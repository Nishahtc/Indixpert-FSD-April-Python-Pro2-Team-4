import uuid
from datetime import datetime
from src.orders.manage_order import ManageOrder
from src.orders.order_model import OrderModel
from src.utility.validations import customer_name_validate, table_number_validate
from src.menu.menu import Menu
from src.booking.table_booking import TableBookingSystem

class OrderFeature(ManageOrder):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        self.table_booking_system = TableBookingSystem()

    def order(self):
        try:
            customer_name = customer_name_validate(input("Enter customer name: "))
            if not customer_name:
                raise ValueError("Invalid customer name.")

            order_type = input("Is this order 'Eat In' or 'Take Out'? ").strip().lower()
            if order_type not in ("eat in", "take out"):
                raise ValueError("Invalid order type. Please enter 'Eat In' or 'Take Out'.")

            items = input("Enter items (comma-separated): ").split(',')
            items = [item.strip() for item in items]

            total_amount = 0
            quantities = []
            for item in items:
                quantity = int(input(f"Enter quantity for {item}: "))
                price = self.menu.get_item_price(item)
                if price is None:
                    print(f"Item '{item}' not found in menu.")
                    continue
                quantities.append(quantity)
                total_amount += price * quantity

            table_number = None
            
            if order_type == "eat in":
                table_number = table_number_validate(input("Enter table number: "))
                if not table_number:
                    raise ValueError("Invalid table number.")
                
                seats_required = int(input("Enter the number of seats required: "))
                self.table_booking_system.book_table(table_number, customer_name, seats_required)
                
            self.add_order(customer_name, table_number, items, quantities, total_amount, order_type)
        except ValueError as error:
            print(error)

    def add_order(self, customer_name, table_number, items, quantity, total_amount, order_type):
        order_id = str(uuid.uuid4())[:6]
        order_date = datetime.now()
        
        if order_type == "take out":
            table_number = None
        
        new_order = OrderModel(order_id, customer_name, table_number, items, quantity, total_amount, order_date, order_type)
        self.orders.append(new_order)
        self.save_order()
        print("Order added successfully.")

    def update_item(self):
        try:
            table_number = table_number_validate(input("Enter table number to update order: "))
            if not table_number:
                raise ValueError("Invalid table number.")

            customer_name = customer_name_validate(input("Enter customer name: "))
            items = input("Enter items (comma-separated): ").split(',')
            items = [item.strip() for item in items]
            
            total_amount = 0
            quantities = []
            for item in items:
                quantity = int(input(f"Enter quantity for {item}: "))
                price = self.menu.get_item_price(item)
                if price is None:
                    print(f"Item '{item}' not found in menu.")
                    continue
                quantities.append(quantity)
                total_amount += price * quantity

            self.update_order(table_number, customer_name, items, quantities, total_amount)
        except ValueError as error:
            print(error)

    def cancel_item(self):
        try:
            table_number = table_number_validate(input("Enter table number to cancel order: "))
            if not table_number:
                raise ValueError("Invalid table number.")
            self.cancel_order(table_number)
        except ValueError as error:
            print(error)

    def search_order_by_table(self):
        try:
            table_number = table_number_validate(input("Enter table number to search for orders: "))
            if not table_number:
                raise ValueError("Invalid table number.")
            
            found_orders = [order for order in self.orders if order.table_number == table_number]
            if found_orders:
                print(f"\nOrders for Table {table_number}:")
                for order in found_orders:
                    print(order)
            else:
                print(f"No orders found for Table {table_number}.")
        except ValueError as error:
            print(error)

    def search_all_orders(self):
        if self.orders:
            print("\nAll Orders:")
            for order in self.orders:
                print(order)
        else:
            print("No orders found.")
            
    def manage_orders(self):
        while True:
            print("\n--- Order Management ---")
            print("1. Add Order")
            print("2. Update Order")
            print("3. Cancel Order")
            print("4. Search Order by Table Number")
            print("5. View All Orders")
            print("6. Go Back to Dashboard")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.order()
            elif choice == '2':
                self.update_item()
            elif choice == '3':
                self.cancel_item()
            elif choice == '4':
                self.search_order_by_table()
                self.prompt_return_to_dashboard()
            elif choice == '5':
                self.search_all_orders()
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
