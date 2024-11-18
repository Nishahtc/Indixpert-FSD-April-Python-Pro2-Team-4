import uuid
from datetime import datetime
from src.orders.manage_order import ManageOrder
from src.orders.order_model import OrderModel
from src.utility.validations import customer_name_validate, table_number_validate
from src.menu.menu import Menu
from src.booking.table_booking import TableBookingSystem
from src.utility.log import log_order
from src.utility.messages import messages

class OrderFeature(ManageOrder):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        self.table_booking_system = TableBookingSystem()

    def order(self):
        try:
            customer_name = customer_name_validate(input("Enter customer name: "))
            if not customer_name:
                raise ValueError(messages.customer_name_invalid)

            print("\nSelect Order Type:")
            print("1. Eat In")
            print("2. Take Out")
            order_type_choice = input("Enter your choice (1 or 2): ").strip()
            
            if order_type_choice == '1':
                order_type = "eat in"
            elif order_type_choice == '2':
                order_type = "take out"
            else:
                print(messages.invalid_choice)
                return

            table_number = None
            time_slot = None

            if order_type == "eat in":
                table_number = table_number_validate(input("Enter table number: "))
                if not table_number:
                    raise ValueError(messages.invalid_table_number)

                self.table_booking_system.tables = self.table_booking_system.load_bookings()
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                bookings_for_today = self.table_booking_system.tables.get(str(table_number), {}).get(current_date, {})
                for slot, booking in bookings_for_today.items():
                    if booking and booking['customer'].lower() == customer_name.lower():
                        time_slot = slot
                        print(f"Existing booking found for customer '{customer_name}' at Table {table_number} for time slot '{time_slot}'.")
                        break
                
                if not time_slot:
                    print(f"\nNo booking found for '{customer_name}' at Table {table_number}. Let's book a table for you.")
                    if not self.book_table_for_order(customer_name, table_number):
                        print(messages.booking_failed)
                        return
            
            items = []
            quantities = []
            total_amount = 0
            
            while True:
                print("\n--- Select Meal Type ---")
                print("Available meal types:")
                for idx, meal_type in enumerate(self.menu.MEAL_TYPES, start=1):
                    print(f"{idx}. {meal_type.title()}")
                print("Enter 'q' to finish adding items.")
                
                meal_choice = input("Enter meal type number (or 'q' to finish): ").strip().lower()
                
                if meal_choice == 'q':
                    break
                try:
                    meal_index = int(meal_choice) - 1
                    if meal_index < 0 or meal_index >= len(self.menu.MEAL_TYPES):
                        print(messages.invalid_choice)
                        continue
                except ValueError:
                    print(messages.invalid_input)
                    continue
                
                selected_meal_type = self.menu.MEAL_TYPES[meal_index]
                
                available_items = self.menu.menu_data.get(selected_meal_type, [])
                if not available_items:
                    print(f"No items available for {selected_meal_type}.")
                    continue
                
                print(f"\nAvailable items in {selected_meal_type.title()}:")
                print(f"{'S.No':<5}{'Item Name':<25}{'Full Price':>10}  {'Half Price':>10}")
                print("-" * 50)
                for idx, item in enumerate(available_items, start=1):
                    half_price = f"{item.half_price:.2f}" if item.half_price else "N/A"
                    print(f"{idx:<5}{item.name:<25}{item.full_price:>10.2f}  {half_price:>10}")

                item_choice = input("Enter item number to add (or 'b' to go back): ").strip().lower()
                if item_choice == 'b':
                    continue
                
                try:
                    item_index = int(item_choice) - 1
                    if item_index < 0 or item_index >= len(available_items):
                        print(messages.invalid_choice)
                        continue
                except ValueError:
                    print(messages.invalid_input)
                    continue
                
                selected_item = available_items[item_index]
                
                try:
                    quantity = int(input(f"Enter quantity for {selected_item.name}: "))
                    if quantity <= 0:
                        print("Quantity must be a positive integer.")
                        continue
                except ValueError:
                    print(messages.invalid_input)
                    continue
                
                if selected_item.half_price is None:
                    portion_size = "full"
                    print(f"Selected portion size: {portion_size}")
                else:
                    portion_size = input(f"Enter portion size for {selected_item.name} (full/half): ").strip().lower()
                    if portion_size not in ['full', 'half']:
                        print(messages.invalid_choice)
                        continue
                
                price = self.menu.get_item_price(selected_item.name, portion_size)
                if price is None:
                    print(f"Item '{selected_item.name}' not found in menu.")
                    continue
                
                items.append(selected_item.name)
                quantities.append(quantity)
                total_amount += price * quantity

                print(f"Added {quantity} x {selected_item.name} ({portion_size}) to the order.")
            
            if not items:
                print(messages.no_items_selected)
                return
            
            self.add_order(customer_name, table_number, items, quantities, total_amount, order_type)
            print(f"\nOrder for customer '{customer_name}' at table {table_number if table_number else 'Take Out'} has been successfully added!")
        except ValueError as error:
            print(f"Error: {error}")

    def book_table_for_order(self, customer_name, table_number):
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        self.table_booking_system.tables = self.table_booking_system.load_bookings()
        
        if str(table_number) not in self.table_booking_system.tables:
            self.table_booking_system.tables[str(table_number)] = {}
        
        if current_date not in self.table_booking_system.tables[str(table_number)]:
            self.table_booking_system.tables[str(table_number)][current_date] = {}
            
        available_slots = [
            slot for slot in self.table_booking_system.TIME_SLOTS 
            if self.table_booking_system.tables[str(table_number)][current_date].get(slot) is None
        ]
        
        if not available_slots:
            print(messages.no_available_slots)
            return False
        
        print("\nAvailable time slots for Table", table_number)
        for idx, slot in enumerate(available_slots, start=1):
            print(f"{idx}. {slot}")
            
        try:
            time_slot_choice = int(input("Enter your choice: ").strip())
            if time_slot_choice < 1 or time_slot_choice > len(available_slots):
                print(messages.invalid_choice)
                return False
        except ValueError:
            print(messages.invalid_input)
            return False
        
        selected_time_slot = available_slots[time_slot_choice - 1]
        
        try:
            seats_requested = int(input("Enter number of seats to book: "))
            if seats_requested <= 0:
                print("Number of seats must be positive.")
                return False
        except ValueError:
            print("Invalid input for number of seats.")
            return False
        
        booking_success = self.table_booking_system.book_table(
            table_number, customer_name, seats_requested, current_date, selected_time_slot
        )
        
        if booking_success:
            print(f"Table {table_number} booked successfully for {customer_name} at {selected_time_slot}.")
            self.table_booking_system.save_bookings()
            return True
        else:
            print("Failed to book the table.")
            return False

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
        print(f"Order added successfully with Order ID: {order_id}")

    def update_item(self):
        try:
            print("\nSearch for Order by:")
            print("1. Table Number")
            print("2. Order ID")
            search_choice = input("Enter your choice: ").strip()
            
            if search_choice == '1':
                search_type = "table"
            elif search_choice == '2':
                search_type = "order_id"
            else:
                print("Invalid choice. Please enter 1 or 2.")
                return
            
            if search_type == "table":
                table_number = table_number_validate(input("Enter table number to update order: "))
                if not table_number:
                    raise ValueError("Invalid table number.")
                found_orders = [order for order in self.orders if order.table_number == table_number]

            elif search_type == "order_id":
                order_id = input("Enter order ID to update: ").strip()
                found_orders = [order for order in self.orders if order.id == order_id]

            else:
                raise ValueError("Invalid choice. Please enter 'table' or 'order_id'.")

            if not found_orders:
                print("No orders found.")
                return

            order = found_orders[0]
            print(f"\n--- Updating Order ID: {order.id} ---")

            items, quantities = [], []

            while True:
                item = input("Enter the item name (leave blank to stop): ").strip()
                if not item:
                    break

                try:
                    quantity = int(input(f"Enter quantity for {item}: "))
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
                    continue

                portion_size = input(f"Enter portion size for {item} (full/half): ").strip().lower()
                if portion_size not in ['full', 'half']:
                    print("Invalid portion size. Try again.")
                    continue

                price = self.menu.get_item_price(item, portion_size)
                if price is None:
                    print(f"Item '{item}' not found in the menu.")
                    continue

                items.append(item)
                quantities.append(quantity)

            if not items:
                print("No items entered. Order update cancelled.")
                return

            order.items = items
            order.quantity = quantities
            order.total_amount = sum(qty * self.menu.get_item_price(item, 'full') for item, qty in zip(items, quantities))

            self.save_order()
            log_order("staff", order.customer_name, items, quantities, order.total_amount)
            print(f"Order ID {order.id} updated successfully!")

        except ValueError as error:
            print(f"Error: {error}")

    def cancel_item(self):
        try:
            print("\nCancel Order by:")
            print("1. Table Number")
            print("2. Order ID")
            cancel_choice = input("Enter your choice (1 or 2): ").strip()
            
            if cancel_choice == '1':
                cancel_type = 'table'
            elif cancel_choice == '2':
                cancel_type = 'order_id'
            else:
                print("Invalid choice. Please enter 1 or 2.")
                return
            
            if cancel_type == "table":
                table_number = table_number_validate(input("Enter table number to cancel order: "))
                if not table_number:
                    raise ValueError("Invalid table number.")
                self.cancel_order_by_table(table_number)

            elif cancel_type == "order_id":
                order_id = input("Enter order ID to cancel: ").strip()
                self.cancel_order_by_id(order_id)
            
            else:
                raise ValueError("Invalid choice. Please enter 'table' or 'order id'.")

        except ValueError as error:
            print(f"Error: {error}")

    def cancel_order_by_table(self, table_number):
        for order in self.orders:
            if order.table_number == table_number:
                self.orders.remove(order)
                self.save_order()
                log_order("staff", order.customer_name, order.items, order.quantity, order.total_amount)
                print(f"Order for Table {table_number} has been cancelled successfully.")
                return
        print(f"No order found for Table {table_number}.")

    def cancel_order_by_id(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                self.orders.remove(order)
                self.save_order()
                log_order("staff", order.customer_name, order.items, order.quantity, order.total_amount)
                print(f"Order with ID {order_id} has been cancelled successfully.")
                return
        print(f"No order found with ID {order_id}.")

    def search_order(self):
        try:
            print("\nSearch for Order by:")
            print("1. Table Number")
            print("2. Order ID")
            search_choice = input("Enter your choice (1 or 2): ").strip()
            
            if search_choice == '1':
                search_type = 'table_number'
            elif search_choice == '2':
                search_type = 'order_id'
            else:
                print("Invalid choice. Please enter 1 or 2.")
                return
            
            if search_type == 'table_number':
                table_number = table_number_validate(input("Enter table number to search for orders: "))
                if not table_number:
                    raise ValueError("Invalid table number.")
                found_orders = [order for order in self.orders if order.table_number == table_number]
                
            elif search_type == "order_id":
                order_id = input("Enter order ID to search for: ").strip()
                found_orders = [order for order in self.orders if order.id == order_id]
                    
            else:
                print("Invalid choice. Please enter 'table number' or 'order id'.")
                return
            
            if found_orders:
                print("\nFound Orders:")
                for order in found_orders:
                    print(order)
            
            else:
                print(messages.no_orders_found)
        except ValueError as error:
            print(f"Error: {error}")
            
            
    def search_all_orders(self):
        if self.orders:
            print("\nAll Orders:")
            for order in self.orders:
                print(order)
        else:
            print(messages.no_orders_found)
