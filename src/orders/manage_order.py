import uuid
from datetime import datetime
from src.orders.order_model import OrderModel
from src.orders.order import Order
from src.utility.messages import messages
from src.utility.log import log_order
from src.utility.validations import table_number_validate
from src.utility.color import bcolors

class ManageOrder(Order):
    def add_order(self, customer_name, table_number, items, quantities, total_amount, order_type):
        order_id = str(uuid.uuid4())[:6]
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if order_type == "take out":
            table_number = None

        new_order = OrderModel(
            id=order_id,
            customer_name=customer_name,
            table_number=table_number,
            items=items,
            quantity=quantities,
            total_amount=total_amount,
            order_date=order_date,
            order_type=order_type
        )
        self.orders.append(new_order)
        self.save_order()
        log_order("staff", customer_name, items, quantities, total_amount)
        print(bcolors.colorize(f"Order added successfully with Order ID: {order_id}",bcolors.LIGHT_GREEN))

    def update_item(self):
        try:
            print(bcolors.colorize("\nSearch for Order by:",bcolors.ORANGE))
            print("1. Table Number")
            print("2. Order ID")
            search_choice = input("Enter your choice: ").strip()
            
            if search_choice == '1':
                search_type = "table"
            elif search_choice == '2':
                search_type = "order_id"
            else:
                print(bcolors.colorize("Invalid choice. Please enter 1 or 2.",bcolors.RED))
                return
            
            if search_type == "table":
                table_number = table_number_validate(input(bcolors.colorize("Enter table number to update order: ",bcolors.TEAL)))
                if not table_number:
                    raise ValueError(bcolors.colorize("Invalid table number.",bcolors.RED))
                found_orders = [order for order in self.orders if order.table_number == table_number]

            elif search_type == "order_id":
                order_id = input(bcolors.colorize("Enter order ID to update: ",bcolors.TEAL)).strip()
                found_orders = [order for order in self.orders if order.id == order_id]

            if not found_orders:
                print(bcolors.colorize("No orders found.",bcolors.LIGHT_YELLOW))
                return

            order = found_orders[0]
            print(bcolors.colorize(f"\n--- Updating Order ID: {order.id} ---",bcolors.LIGHT_GREEN))

            items =[]
            quantities = [] 

            while True:
                item = input(bcolors.colorize("Enter the item name (leave blank to stop): ",bcolors.TEAL)).strip()
                if not item:
                    break

                try:
                    quantity = int(input(bcolors.colorize(f"Enter quantity for {item}: ",bcolors.TEAL)))
                except ValueError:
                    print(bcolors.colorize("Invalid quantity. Please enter a number.",bcolors.RED))
                    continue

                portion_size = input(bcolors.colorize(f"Enter portion size for {item} (full/half): ",bcolors.TEAL)).strip().lower()
                if portion_size not in ['full', 'half']:
                    print(bcolors.colorize("Invalid portion size. Try again.",bcolors.RED))
                    continue

                price = self.menu.get_item_price(item, portion_size)
                if price is None:
                    print(bcolors.colorize(f"Item '{item}' not found in the menu.",bcolors.LIGHT_YELLOW))
                    continue

                items.append(item)
                quantities.append(quantity)

            if not items:
                print(bcolors.colorize("No items entered. Order update cancelled.",bcolors.LIGHT_YELLOW))
                return

            order.items = items
            order.quantity = quantities
            order.total_amount = sum(qty * self.menu.get_item_price(item, 'full') for item, qty in zip(items, quantities))

            self.save_order()
            log_order("staff", order.customer_name, items, quantities, order.total_amount)
            print(bcolors.colorize(f"Order ID {order.id} updated successfully!",bcolors.LIGHT_GREEN))

        except ValueError as error:
            print(bcolors.colorize(f"Error: {error}",bcolors.RED))

    def cancel_item(self):
        try:
            print(bcolors.colorize("\nCancel Order by:",bcolors.ORANGE))
            print("1. Table Number")
            print("2. Order ID")
            cancel_choice = input(bcolors.colorize("Enter your choice (1 or 2): ",bcolors.TEAL)).strip()
            
            if cancel_choice == '1':
                cancel_type = 'table'
            elif cancel_choice == '2':
                cancel_type = 'order_id'
            else:
                print(bcolors.colorize("Invalid choice. Please enter 1 or 2.",bcolors.RED))
                return
            
            if cancel_type == "table":
                table_number = table_number_validate(input(bcolors.colorize("Enter table number to cancel order: ",bcolors.TEAL)))
                if not table_number:
                    raise ValueError(bcolors.colorize("Invalid table number.",bcolors.RED))
                self.cancel_order_by_table(table_number)

            elif cancel_type == "order_id":
                order_id = input(bcolors.colorize("Enter order ID to cancel: ",bcolors.TEAL)).strip()
                self.cancel_order_by_id(order_id)

        except ValueError as error:
            print(bcolors.colorize(f"Error: {error}",bcolors.RED))

    def cancel_order_by_table(self, table_number):
        for order in self.orders:
            if order.table_number == table_number:
                self.orders.remove(order)
                self.save_order()
                log_order("staff", order.customer_name, order.items, order.quantity, order.total_amount)
                print(bcolors.colorize(f"Order for Table {table_number} has been cancelled successfully.",bcolors.LIGHT_YELLOW))
                return
        print(bcolors.colorize(f"No order found for Table {table_number}.",bcolors.LIGHT_YELLOW))

    def cancel_order_by_id(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                self.orders.remove(order)
                self.save_order()
                log_order("staff", order.customer_name, order.items, order.quantity, order.total_amount)
                print(bcolors.colorize(f"Order with ID {order_id} has been cancelled successfully.",bcolors.LIGHT_GREEN))
                return
        print(bcolors.colorize(f"No order found with ID {order_id}.",bcolors.LIGHT_YELLOW))

    def search_order(self):
        try:
            print(bcolors.colorize("\nSearch for Order by:",bcolors.ORANGE))
            print("1. Table Number")
            print("2. Order ID")
            search_choice = input("Enter your choice: ").strip()
            
            if search_choice == '1':
                search_type = 'table_number'
            elif search_choice == '2':
                search_type = 'order_id'
            else:
                print(bcolors.colorize("Invalid choice. Please enter 1 or 2.",bcolors.RED))
                return
            
            if search_type == 'table_number':
                table_number = table_number_validate(input(bcolors.colorize("Enter table number to search for orders: ",bcolors.TEAL)))
                if not table_number:
                    raise ValueError(bcolors.colorize("Invalid table number.",bcolors.RED))
                found_orders = [order for order in self.orders if order.table_number == table_number]
                
            elif search_type == "order_id":
                order_id = input(bcolors.colorize("Enter order ID to search for: ",bcolors.TEAL)).strip()
                found_orders = [order for order in self.orders if order.id == order_id]
                    
            if found_orders:
                print(bcolors.colorize("\nFound Orders:",bcolors.ORANGE))
                for order in found_orders:
                    print(order)
            else:
                print(messages.no_orders_found)

        except ValueError as error:
            print(bcolors.colorize(f"Error: {error}",bcolors.RED))
            
    def search_all_orders(self):
        if self.orders:
            print(bcolors.colorize("\nAll Orders:",bcolors.ORANGE))
            for order in self.orders:
                print(order)
        else:
            print(messages.no_orders_found)
