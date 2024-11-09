import json
import os
from src.utility.validations import customer_name_validate

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
                print("Error loading table bookings. Starting with an empty table booking list.")
        return {str(i): {'customer': None, 'seats': 5} for i in range(1, 6)}

    def save_bookings(self):
        try:
            with open(TABLE_BOOKING_FILE, 'w') as file:
                json.dump(self.tables, file, indent=4)
            print("Booking data saved successfully.")
        except Exception as e:
            print(f"Error saving booking data: {e}")
    

    def view_available_tables(self):
        print("\nAvailable Tables:")
        for table, info in self.tables.items():
            if info['customer'] is None:
                print(f"Table {table} is available with {info['seats']} seats.")
            else:
                print(f"Table {table} is booked by {info['customer']} with {info['seats']} seats remaining.")

    def book_table(self, table_number, customer_name, seats_requested):
        table_number = str(table_number)
        if table_number not in self.tables:
            print("Invalid table number.")

        validated_name = customer_name_validate(customer_name)
        if not validated_name:
            print("Invalid customer name. Please use only alphabetic characters.")

        table_info = self.tables[table_number]
        if table_info['customer'] is None or table_info['customer'] == validated_name:
            if seats_requested <= table_info['seats']:
                table_info['customer'] = validated_name
                table_info['seats'] -= seats_requested
                self.save_bookings()
                print(f"Table {table_number} has been booked by {validated_name} for {seats_requested} seats.")
            else:
                print(f"Only {table_info['seats']} seats available at Table {table_number}.")
        else:
            print(f"Table {table_number} is already booked by {table_info['customer']}.")

    def cancel_booking(self, table_number):
        table_number = str(table_number)
        if table_number not in self.tables:
            print("Invalid table number.")

        table_info = self.tables[table_number]
        if table_info['customer'] is not None:
            customer_name = table_info['customer']
            print(f"Cancelling booking for Table {table_number} booked by {customer_name}.")
            self.tables[table_number]['customer'] = None
            self.tables[table_number]['seats'] = 5
            self.save_bookings()
            print(f"Booking for Table {table_number} has been cancelled successfully.")
        else:
            print(f"Table {table_number} is already available.")

    def manage_bookings(self):
        while True:
            print("\n--- Table Booking Management ---")
            print("1. View All Tables")
            print("2. Book a Table")
            print("3. Cancel a Booking")
            print("4. Go Back to Dashboard")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_available_tables()
                self.prompt_return_to_dashboard()
            elif choice == '2':
                try:
                    table_number = int(input("Enter table number to book: "))
                    customer_name = input("Enter customer name: ")
                    seats_requested = int(input("Enter number of seats to book: "))
                    self.book_table(table_number, customer_name, seats_requested)
                except ValueError:
                    print("Invalid input. Please enter numeric values for table number and seats.")
            elif choice == '3':
                try:
                    table_number = int(input("Enter table number to cancel: "))
                    self.cancel_booking(table_number)
                except ValueError:
                    print("Invalid input. Please enter a numeric table number.")
            elif choice == '4':
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
