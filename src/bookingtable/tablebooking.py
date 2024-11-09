import json
import os

class TableBookingSystem:
    def __init__(self):  
        
        self.tables = {i: None for i in range(1, 9)}  
        self.load_tables()

    def load_tables(self):
        """Load table reservations from a JSON file if it exists."""
        if os.path.exists('tables.json'):
            with open('tables.json', 'r') as file:
                try:
                    loaded_tables = json.load(file)
                    
                    if isinstance(loaded_tables, dict) and all(key in range(1, 9) for key in loaded_tables.keys()):
                        self.tables = loaded_tables
                        print("Table reservations loaded from tables.json.")
                    else:
                        print("Error: Loaded data is not in the expected format, starting with empty tables.")
                except json.JSONDecodeError:
                    print("Error: Failed to parse tables.json, starting with empty tables.")
        else:
            print("No previous table reservations found, starting with empty tables.")

    def save_tables(self):
        """Save table reservations to a JSON file."""
        with open('tables.json', 'w') as file:
            json.dump(self.tables, file)
            print("Table reservations saved to tables.json.")

    def view_available_tables(self):
        print("\nAvailable Tables:")
        for table_number, reservation in self.tables.items():
            status = "available" if reservation is None else f"booked by {reservation}"
            print(f"Table {table_number} is {status}")

    def book_table(self, table_number, customer_name):
        if table_number in self.tables:
            if self.tables[table_number] is None:
                self.tables[table_number] = customer_name
                self.save_tables()  
                print(f"Table {table_number} has been booked by {customer_name}.")
            else:
                print(f"Table {table_number} is already booked by {self.tables[table_number]}.")
        else:
            print(f"Error: Table {table_number} is invalid.")  # Improved error message

    def cancel_booking(self, table_number):
        if table_number in self.tables:
            if self.tables[table_number] is not None:
                customer_name = self.tables[table_number]
                self.tables[table_number] = None
                self.save_tables()  
                print(f"Booking for Table {table_number} by {customer_name} has been canceled.")
            else:
                print(f"Table {table_number} is not booked.")
        else:
            print(f"Error: Table {table_number} is invalid.")  # Improved error message

    def manage_bookings(self):
        while True:
            print("\n--- Staff Management Menu ---") 
            print("1. View All Tables")
            print("2. Cancel a Booking")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_available_tables()
            elif choice == '2':
                try:
                    table_number = int(input("Enter table number to cancel: "))
                    self.cancel_booking(table_number)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '3':
                print("Exiting staff management.")
                break
            else:
                print("Invalid choice. Please try again.")

    def customer_menu(self):
        while True:
            print("\n--- Customer Menu ---")
            print("1. View Available Tables")
            print("2. Book a Table")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_available_tables()
            elif choice == '2':
                try:
                    table_number = int(input("Enter table number to book: "))
                    customer_name = input("Enter your name: ")
                    self.book_table(table_number, customer_name)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '3':
                print("Exiting customer menu.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__": 
    system = TableBookingSystem()
    while True:
        print("\n--- Main Menu ---")
        print("1. Customer Menu")
        print("2. Staff Management Menu")
        print("3. Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == '1':
            system.customer_menu()
        elif main_choice == '2':
            system.manage_bookings()
        elif main_choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

