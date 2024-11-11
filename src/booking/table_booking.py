import json
import os
from src.utility.validations import customer_name_validate
from src.utility.messages import Messages

DATABASE_FOLDER = "src/database"
TABLE_BOOKING_FILE = os.path.join(DATABASE_FOLDER, "booking.json")

class TableBookingSystem:
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
        return {str(i): {'customer': None, 'seats': 5} for i in range(1, 6)}

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
            if info['customer'] is None:
                Messages.table_available(table, info['seats'])
            else:
                Messages.table_booked(table, info['customer'], info['seats'])

    def book_table(self, table_number, customer_name, seats_requested):
        table_number = str(table_number)
        if table_number not in self.tables:
            Messages.invalid_table_number()
            return

        validated_name = customer_name_validate(customer_name)
        if not validated_name:
            Messages.invalid_customer_name()
            return

        table_info = self.tables[table_number]
        if table_info['customer'] is None or table_info['customer'] == validated_name:
            if seats_requested <= table_info['seats']:
                table_info['customer'] = validated_name
                table_info['seats'] -= seats_requested
                self.save_bookings()
                Messages.table_booked_successfully(table_number, validated_name, seats_requested)
            else:
                Messages.insufficient_seats(table_number, table_info['seats'])
        else:
            Messages.table_already_booked(table_number, table_info['customer'])

    def cancel_booking(self, table_number):
        table_number = str(table_number)
        if table_number not in self.tables:
            Messages.invalid_table_number()
            return

        table_info = self.tables[table_number]
        if table_info['customer'] is not None:
            customer_name = table_info['customer']
            Messages.cancelling_booking(table_number, customer_name)
            self.tables[table_number]['customer'] = None
            self.tables[table_number]['seats'] = 5
            self.save_bookings()
            Messages.booking_cancelled(table_number)
        else:
            Messages.table_already_available(table_number)

    def manage_bookings(self):
        while True:
            Messages.booking_management_menu()

            choice = input(Messages.enter_choice())

            if choice == '1':
                self.view_available_tables()
                self.prompt_return_to_dashboard()
            elif choice == '2':
                try:
                    table_number = int(input(Messages.enter_table_number()))
                    customer_name = input(Messages.enter_customer_name())
                    seats_requested = int(input(Messages.enter_seats_requested()))
                    self.book_table(table_number, customer_name, seats_requested)
                except ValueError:
                    Messages.invalid_numeric_input()
            elif choice == '3':
                try:
                    table_number = int(input(Messages.enter_table_number_to_cancel()))
                    self.cancel_booking(table_number)
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
