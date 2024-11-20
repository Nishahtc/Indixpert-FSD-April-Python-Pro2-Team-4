import json
import os
from datetime import datetime, timedelta
from src.utility.validations import customer_name_validate, has_reached_booking_limit
from src.utility.messages import messages
from src.utility.color import bcolors

DATABASE_FOLDER = "src/database"
TABLE_BOOKING_FILE = os.path.join(DATABASE_FOLDER, "booking.json")

class TableBookingSystem:
    TIME_SLOTS = ["12:00-14:00", "14:00-16:00", "18:00-20:00", "20:00-22:00"]

    def __init__(self):
        if not os.path.exists(DATABASE_FOLDER):
            os.makedirs(DATABASE_FOLDER)
        self.tables = self.load_bookings()

    def load_bookings(self):
        if os.path.exists(TABLE_BOOKING_FILE):
            try:
                with open(TABLE_BOOKING_FILE, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(messages.data_load_error)
        return {str(i): {'customer': None, 'seats': 5, 'bookings': {slot: None for slot in self.TIME_SLOTS}} for i in range(1, 6)}

    def save_bookings(self):
        try:
            with open(TABLE_BOOKING_FILE, 'w') as file:
                json.dump(self.tables, file, indent=4)
            print(messages.booking_save_success)
        except Exception:
            print(messages.data_save_error)
            

    def view_available_tables(self):
        print(bcolors.colorize("\nAvailable Tables:", bcolors.LIGHT_GREEN))
        
        upcoming_dates = self.generate_date_options()
        
        for table, info in self.tables.items():
            print(f"\nTable {table}:")
            has_bookings = False
            
            for date in upcoming_dates:
                if date in info:
                    has_bookings = True
                    print(f" Date: {date}")
                    for time_slot, booking in info[date].items():
                        if booking is None:
                            print(bcolors.colorize(f"Time Slot {time_slot} is available.",bcolors.LIGHT_YELLOW))
                        else:
                            customer = booking['customer']
                            seats = booking['seats']
                            print(bcolors.colorize(f"Time Slot {time_slot} is booked by {customer} for {seats} seats.",bcolors.LIGHT_GREEN))
                            
            if not has_bookings:
                print(messages.no_bookings)

    def book_table(self, table_number, customer_name, seats_requested, date, time_slot):
        table_number = str(table_number)
        
        if table_number not in self.tables:
            print(messages.invalid_table_number)
            return False
        
        self.tables = self.load_bookings()
        
        validated_name = customer_name_validate(customer_name)
        if not validated_name:
            print(messages.customer_name_invalid)
            return False
        
        if has_reached_booking_limit(customer_name):
            print(bcolors.colorize("Booking limit reached! You cannot book more than 5 tables.",bcolors.LIGHT_YELLOW))
            return False
        
        if seats_requested > 5:
            print(bcolors.colorize("Seat booking limit exceeded! You cannot book more than 5 seats.",bcolors.LIGHT_YELLOW))
            return False
        
        if date not in self.tables[table_number]:
            self.tables[table_number][date] = {}
        
        if self.tables[table_number][date].get(time_slot):
            print(messages.table_already_booked.format(time_slot, date))
            return False
        
        self.tables[table_number][date][time_slot] = {
            'customer': validated_name,
            'seats': seats_requested
        }
        self.save_bookings()
        print(messages.table_booking_success.format(table_number, validated_name, seats_requested, date, time_slot))
        return True
    
    def generate_date_options(self, days=7):
        today = datetime.now()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

    # def is_table_booked(self, table_number, customer_name, time_slot):
    #     table_number = str(table_number)
    #     current_date = datetime.now().strftime("%Y-%m-%d")
        
    #     self.tables = self.load_bookings()
    #     if table_number not in self.tables or current_date not in self.tables[table_number]:
    #         return False
        
    #     bookings_for_today = self.tables[table_number][current_date]
    #     for time_slot, booking in bookings_for_today.items():
    #         if booking and booking['customer'].lower() == customer_name.lower():
    #             return time_slot
    #     return None

    def cancel_booking(self, table_number):
        table_number = str(table_number)

        if table_number not in self.tables:
            print(messages.invalid_table_number)
            return False

        self.tables = self.load_bookings()
        bookings = self.tables[table_number]
        
        booked_entries = []
        for date, slots in bookings.items():
            if date == 'bookings':
                continue
            for time_slot, details in slots.items():
                if details is not None:
                    booked_entries.append((date, time_slot, details['customer']))
        
        if not booked_entries:
            print(messages.booking_not_found)
            return False
        
        print(bcolors.colorize(f"\nCurrent bookings for Table {table_number}:"),bcolors.ORANGE)
        for index, (date, time_slot, customer) in enumerate(booked_entries, start=1):
            print(bcolors.colorize(f"{index}. Date: {date}, Time Slot: {time_slot}, Customer: {customer}",bcolors.CYAN))
            
        try:
            choice = int(input(bcolors.colorize("Enter your choice to cancel (1, 2, 3, etc.): ",bcolors.TEAL)).strip())
            if choice < 1 or choice > len(booked_entries):
                print(messages.invalid_choice)
                return False
        except ValueError:
            print(messages.invalid_input)
            return False
        
        selected_date, selected_slot, customer_name = booked_entries[choice - 1]
        print(bcolors.colorize(f"Cancelling booking for Table {table_number} on {selected_date} at {selected_slot} by {customer_name}.",bcolors.LIGHT_YELLOW))
        del self.tables[table_number][selected_date][selected_slot]
        
        if not self.tables[table_number][selected_date]:
            del self.tables[table_number][selected_date]
        
        self.save_bookings()
        print(messages.booking_cancel_success.format(table_number, selected_date, selected_slot))
        return True

    def manage_bookings(self):
        while True:
            print(bcolors.colorize("\n--- Table Booking Management ---",bcolors.ORANGE))
            print("1. View All Tables")
            print("2. Book a Table")
            print("3. Cancel a Booking")
            print("4. Go Back to Dashboard")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.view_available_tables()
                self.prompt_return_to_dashboard()
            elif choice == '2':
                try:
                    table_number = int(input(bcolors.colorize("Enter table number to book: ",bcolors.TEAL)))
                    customer_name = input(bcolors.colorize("Enter customer name: ",bcolors.TEAL))
                    seats_requested = int(input(bcolors.colorize("Enter number of seats to book: ",bcolors.TEAL)))
                    
                    print(bcolors.colorize("\nAvailable dates:",bcolors.ORANGE))
                    upcoming_dates = self.generate_date_options()
                    for idx, date in enumerate(upcoming_dates, start=1):
                        print(f"{idx}. {date}")
                    
                    date_choice = int(input(bcolors.colorize("Enter your choice for date: ",bcolors.TEAL)).strip())
                    if date_choice < 1 or date_choice > len(upcoming_dates):
                        print(bcolors.colorize("Invalid choice. Please select a valid date.",bcolors.RED))
                        return
                    
                    selected_date = upcoming_dates[date_choice - 1]
                    
                    print(bcolors.colorize("\nAvailable time slots:",bcolors.ORANGE))
                    available_slots = [slot for slot in self.TIME_SLOTS if
                                       self.tables[str(table_number)].get(selected_date, {}).get(slot) is None]
                    
                    if not available_slots:
                        print(bcolors.colorize("No available time slots for the selected table on this date.",bcolors.LIGHT_YELLOW))
                        return
                    
                    for idx, slot in enumerate(available_slots, start=1):
                        print(bcolors.colorize(f"{idx}. {slot}",bcolors.CYAN))
                    
                    time_slot_choice = int(input(bcolors.colorize("Enter your choice for time slot: ",bcolors.TEAL)).strip())
                    if time_slot_choice < 1 or time_slot_choice > len(available_slots):
                        print(messages.invalid_choice)
                        return
                    
                    selected_time_slot = available_slots[time_slot_choice - 1]
                    
                    self.book_table(table_number, customer_name, seats_requested, selected_date, selected_time_slot)

                except ValueError:
                    print(messages.invalid_input)
            
            elif choice == '3':
                try:
                    table_number = int(input(bcolors.colorize("Enter table number to cancel: ",bcolors.TEAL)))
                    self.cancel_booking(table_number)
                except ValueError:
                    print(messages.invalid_input)
            elif choice == '4':
                print(messages.exiting_system)
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
