import json
import os
from src.utility.validations import customer_name_validate
from src.utility.messages import Messages

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
                Messages.error_loading_bookings()
        return {str(i): {'customer': None, 'seats': 5, 'bookings': {slot: None for slot in self.TIME_SLOTS}} for i in range(1, 6)}

    def save_bookings(self):
        try:
            with open(TABLE_BOOKING_FILE, 'w') as file:
                json.dump(self.tables, file, indent=4)
            Messages.booking_saved()
        except Exception as e:
            Messages.error_saving_bookings(e)

    def view_available_tables(self):
        Messages.available_tables()
        for table, info in self.tables.items():
            print(f"\nTable {table}:")
            for time_slot, booking in info['bookings'].items():
                if booking is None:
                    Messages.time_slot_available(time_slot)
                else:
                    customer = booking['customer']
                    seats = booking['seats']
                    Messages.time_slot_booked(time_slot, customer, seats)

    def book_table(self, table_number, customer_name, seats_requested, time_slot):
        table_number = str(table_number)

        if table_number not in self.tables:
            Messages.invalid_table_number()
            return False
        if time_slot not in self.TIME_SLOTS:
            Messages.invalid_time_slot()
            return False

        if self.tables[table_number]['bookings'][time_slot] is not None:
            Messages.time_slot_already_booked()
            return False

        validated_name = customer_name_validate(customer_name)
        if not validated_name:
            Messages.invalid_customer_name()
            return False

        self.tables[table_number]['bookings'][time_slot] = {
            'customer': validated_name,
            'seats': seats_requested
        }
        self.save_bookings()
        Messages.table_booked_successfully(table_number, validated_name, seats_requested)
        return True

    def is_table_booked(self, table_number, customer_name, time_slot):
        table_number = str(table_number)
        self.tables = self.load_bookings()
        if table_number not in self.tables:
            return False
        booking = self.tables[table_number]['bookings'].get(time_slot)
        if booking is None:
            return False
        return booking['customer'].lower() == customer_name.lower()

    def cancel_booking(self, table_number, time_slot):
        table_number = str(table_number)

        if table_number not in self.tables:
            Messages.invalid_table_number()
            return False

        if time_slot not in self.TIME_SLOTS:
            Messages.invalid_time_slot()
            return False

        if self.tables[table_number]['bookings'][time_slot] is None:
            Messages.no_booking_found()
            return False

        customer_name = self.tables[table_number]['bookings'][time_slot]['customer']
        Messages.cancelling_booking(table_number, customer_name)
        self.tables[table_number]['bookings'][time_slot] = None
        self.save_bookings()
        Messages.booking_cancelled(table_number)
        return True

    def manage_bookings(self):
        while True:
            Messages.booking_management_menu()
            choice = input(Messages.enter_choice()).strip()

            if choice == '1':
                self.view_available_tables()
                self.prompt_return_to_dashboard()
            elif choice == '2':
                try:
                    table_number = int(input(Messages.enter_table_number()))
                    customer_name = input(Messages.enter_customer_name())
                    seats_requested = int(input(Messages.enter_seats_requested()))
                    time_slot = input(Messages.enter_time_slot()).strip()
                    self.book_table(table_number, customer_name, seats_requested, time_slot)
                except ValueError:
                    Messages.invalid_numeric_input()
            elif choice == '3':
                try:
                    table_number = int(input(Messages.enter_table_number_to_cancel()))
                    time_slot = input(Messages.enter_time_slot()).strip()
                    self.cancel_booking(table_number, time_slot)
                except ValueError:
                    Messages.invalid_numeric_input()
            elif choice == '4':
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
