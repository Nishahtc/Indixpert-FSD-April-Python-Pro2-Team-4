class TableBookingSystem:
    def __init__(self):
        self.tables = {1: None, 2: None, 3: None, 4: None, 5: None}

    def view_available_tables(self):
        print("\nAvailable Tables:")
        for table, reservation in self.tables.items():
            if reservation is None:
                print(f"Table {table} is available")
            else:
                print(f"Table {table} is booked by {reservation}")

    def book_table(self, table_number, customer_name):
        if table_number in self.tables:
            if self.tables[table_number] is None:
                self.tables[table_number] = customer_name
                print(f"Table {table_number} has been booked by {customer_name}.")
            else:
                print(f"Table {table_number} is already booked by {self.tables[table_number]}.")
        else:
            print("Invalid table number.")

    def cancel_booking(self, table_number):
        if table_number in self.tables:
            if self.tables[table_number] is not None:
                customer_name = self.tables[table_number]
                self.tables[table_number] = None
                print(f"Booking for Table {table_number} by {customer_name} has been canceled.")
            else:
                print(f"Table {table_number} is not booked.")
        else:
            print("Invalid table number.")

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
                table_number = int(input("Enter table number to cancel: "))
                self.cancel_booking(table_number)
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
                table_number = int(input("Enter table number to book: "))
                customer_name = input("Enter your name: ")
                self.book_table(table_number, customer_name)
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
