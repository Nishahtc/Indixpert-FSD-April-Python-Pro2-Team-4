import uuid
from datetime import datetime
from src.orders.manage_order import ManageOrder
from src.utility.validations import customer_name_validate, table_number_validate
from src.menu.menu import Menu
from src.booking.table_booking import TableBookingSystem
from src.utility.messages import messages
from src.utility.color import bcolors


class OrderFeature(ManageOrder):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        self.table_booking_system = TableBookingSystem()

    def order(self):
        try:
            customer_name = customer_name_validate(input(bcolors.colorize("Enter customer name: ",bcolors.TEAL)))
            if not customer_name:
                raise ValueError(messages.customer_name_invalid)

            print(bcolors.colorize("\nSelect Order Type:",bcolors.ORANGE))
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
                table_number = table_number_validate(input(bcolors.colorize("Enter table number: ",bcolors.TEAL)))
                if not table_number:
                    raise ValueError(messages.invalid_table_number)

                self.table_booking_system.tables = self.table_booking_system.load_bookings()
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                bookings_for_today = self.table_booking_system.tables.get(str(table_number), {}).get(current_date, {})
                for slot, booking in bookings_for_today.items():
                    if booking and booking['customer'].lower() == customer_name.lower():
                        time_slot = slot
                        print(bcolors.colorize(f"Existing booking found for customer '{customer_name}' at Table {table_number} for time slot '{time_slot}'.",bcolors.LIGHT_YELLOW))
                        break
                
                if not time_slot:
                    print(bcolors.colorize(f"\nNo booking found for '{customer_name}' at Table {table_number}. Let's book a table for you.",bcolors.LIGHT_YELLOW))
                    if not self.book_table_for_order(customer_name, table_number):
                        print(messages.booking_failed)
                        return
            
            items = []
            quantities = []
            total_amount = 0
            
            while True:
                print(bcolors.colorize("\n--- Select Meal Type ---",bcolors.LIGHT_GREEN))
                print(bcolors.colorize("Available meal types:",bcolors.ORANGE))
                for idx, meal_type in enumerate(self.menu.MEAL_TYPES, start=1):
                    print(bcolors.colorize(f"{idx}. {meal_type.title()}",bcolors.CYAN))
                print(bcolors.colorize("Enter 'q' to finish adding items.",bcolors.LIGHT_YELLOW))
                
                meal_choice = input(bcolors.colorize("Enter meal type number (or 'q' to finish): ",bcolors.TEAL)).strip().lower()
                
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
                    print(bcolors.colorize(f"No items available for {selected_meal_type}.",bcolors.LIGHT_YELLOW))
                    continue
                
                print(bcolors.colorize(f"\nAvailable items in {selected_meal_type.title()}:",bcolors.ORANGE))
                print(bcolors.colorize(f"{'S.No':<5}{'Item Name':<25}{'Full Price':>10}  {'Half Price':>10}",bcolors.CYAN))
                print("-" * 50)
                for idx, item in enumerate(available_items, start=1):
                    half_price = bcolors.colorize(f"{int(item.half_price)}",bcolors.CYAN) if item.half_price else "N/A"
                    print(bcolors.colorize(f"{idx:<5}{item.name:<25}{int(item.full_price):>10}  {half_price:>10}",bcolors.CYAN))

                item_choice = input(bcolors.colorize("Enter item number to add (or 'b' to go back): ",bcolors.TEAL)).strip().lower()
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
                    quantity = int(input(bcolors.colorize(f"Enter quantity for {selected_item.name}: ",bcolors.TEAL)))
                    if quantity <= 0:
                        print(bcolors.colorize("Quantity must be a positive integer.",bcolors.LIGHT_YELLOW))
                        continue
                except ValueError:
                    print(messages.invalid_input)
                    continue
                
                if selected_item.half_price is None:
                    portion_size = "full"
                    print(bcolors.colorize(f"Selected portion size: {portion_size}",bcolors.LIGHT_YELLOW))
                else:
                    portion_size = input(bcolors.colorize(f"Enter portion size for {selected_item.name} (full/half): ",bcolors.TEAL)).strip().lower()
                    if portion_size not in ['full', 'half']:
                        print(messages.invalid_choice)
                        continue
                
                price = self.menu.get_item_price(selected_item.name, portion_size)
                if price is None:
                    print(bcolors.colorize(f"Item '{selected_item.name}' not found in menu.",bcolors.LIGHT_YELLOW))
                    continue
                
                items.append(selected_item.name)
                quantities.append(quantity)
                total_amount += price * quantity

                print(bcolors.colorize(f"Added {quantity} x {selected_item.name} ({portion_size}) to the order.",bcolors.LIGHT_GREEN))
            
            if not items:
                print(messages.no_items_selected)
                return
            
            
            super().add_order(customer_name, table_number, items, quantities, total_amount, order_type)
            print(bcolors.colorize(f"\nOrder for customer '{customer_name}' at table {table_number if table_number else 'Take Out'} has been successfully added!",bcolors.colorize))
        except ValueError as error:
            print(bcolors.colorize(f"Error: {error}",bcolors.RED))

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
        
        print(bcolors.colorize("\nAvailable time slots for Table",bcolors.LIGHT_YELLOW), table_number)
        for idx, slot in enumerate(available_slots, start=1):
            print(bcolors.colorize(f"{idx}. {slot}",bcolors.CYAN))
            
        try:
            time_slot_choice = int(input(bcolors.colorize("Enter your choice: ",bcolors.TEAL)).strip())
            if time_slot_choice < 1 or time_slot_choice > len(available_slots):
                print(messages.invalid_choice)
                return False
        except ValueError:
            print(messages.invalid_input)
            return False
        
        selected_time_slot = available_slots[time_slot_choice - 1]
        
        try:
            seats_requested = int(input(bcolors.colorize("Enter number of seats to book: ",bcolors.TEAL)))
            if seats_requested <= 0:
                print(bcolors.colorize("Number of seats must be positive.",bcolors.LIGHT_YELLOW))
                return False
        except ValueError:
            print(bcolors.colorize("Invalid input for number of seats.",bcolors.RED))
            return False
        
        booking_success = self.table_booking_system.book_table(
            table_number, customer_name, seats_requested, current_date, selected_time_slot
        )
        
        if booking_success:
            print(bcolors.colorize(f"Table {table_number} booked successfully for {customer_name} at {selected_time_slot}.",bcolors.LIGHT_GREEN))
            self.table_booking_system.save_bookings()
            return True
        else:
            print(bcolors.colorize("Failed to book the table.",bcolors.LIGHT_YELLOW))
            return False
