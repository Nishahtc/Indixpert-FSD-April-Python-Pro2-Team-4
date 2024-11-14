class Messages:
    # user_auth start
    @staticmethod
    def enter_username():
        return "Enter username: "

    @staticmethod
    def enter_password():
        return "Enter password: "

    @staticmethod
    def enter_first_name():
        return "Enter first name: "

    @staticmethod
    def enter_last_name():
        return "Enter last name: "

    @staticmethod
    def welcome_back(username):
        print(f"Welcome back, {username}!")

    @staticmethod
    def invalid_credentials():
        print("Invalid credentials.")

    @staticmethod
    def username_exists():
        print("Username already exists. Try a different one.")

    @staticmethod
    def signup_success(username, role):
        print(f"User {username} signed up successfully as {role}.")

    @staticmethod
    def manage_users_menu():
        print("\n--- Manage Users ---")
        print("1. View All Users")
        print("2. Add New User")
        print("3. Delete User")
        print("4. Back to Admin Menu")

    @staticmethod
    def choose_option():
        return "Choose an option: "

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")

    @staticmethod
    def registered_users():
        print("\nRegistered Users:")

    @staticmethod
    def no_users():
        print("No registered users found.")

    # @staticmethod
    # def user_details(username, role):
    #     print(f"Username: {username}, Role: {role}")

    @staticmethod
    def enter_username_to_delete():
        return "Enter the username of the user to delete: "

    @staticmethod
    def user_deleted(username):
        print(f"User '{username}' deleted successfully.")

    @staticmethod
    def user_not_found(username):
        print(f"User '{username}' not found.")

    @staticmethod
    def welcome_system():
        print("\n***** Welcome to the System *****")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

    @staticmethod
    def exit_system():
        print("Exiting the system.")
    # user_auth end
    
    
    #table_booking start
    @staticmethod
    def error_loading_bookings():
        print("Error loading table bookings. Starting with an empty table booking list.")

    @staticmethod
    def booking_saved():
        print("Booking data saved successfully.")

    @staticmethod
    def error_saving_bookings(error):
        print(f"Error saving booking data: {error}")

    @staticmethod
    def available_tables():
        print("\nAvailable Tables:")

    @staticmethod
    def table_available(table, seats):
        print(f"Table {table} is available with {seats} seats.")

    @staticmethod
    def table_booked(table, customer, seats):
        print(f"Table {table} is booked by {customer} with {seats} seats remaining.")

    @staticmethod
    def invalid_table_number():
        print("Invalid table number.")

    @staticmethod
    def invalid_customer_name():
        print("Invalid customer name. Please use only alphabetic characters.")

    @staticmethod
    def table_booked_successfully(table_number, customer_name, seats_requested):
        print(f"Table {table_number} has been booked by {customer_name} for {seats_requested} seats.")

    @staticmethod
    def insufficient_seats(table_number, seats):
        print(f"Only {seats} seats available at Table {table_number}.")

    @staticmethod
    def table_already_booked(table_number, customer):
        print(f"Table {table_number} is already booked by {customer}.")

    @staticmethod
    def cancelling_booking(table_number, customer_name):
        print(f"Cancelling booking for Table {table_number} booked by {customer_name}.")

    @staticmethod
    def booking_cancelled(table_number):
        print(f"Booking for Table {table_number} has been cancelled successfully.")

    @staticmethod
    def table_already_available(table_number):
        print(f"Table {table_number} is already available.")

    @staticmethod
    def booking_management_menu():
        print("\n--- Table Booking Management ---")
        print("1. View All Tables")
        print("2. Book a Table")
        print("3. Cancel a Booking")
        print("4. Go Back to Dashboard")

    @staticmethod
    def enter_choice():
        return "Enter your choice: "

    @staticmethod
    def enter_table_number():
        return "Enter table number to book: "

    @staticmethod
    def enter_customer_name():
        return "Enter customer name: "

    @staticmethod
    def enter_seats_requested():
        return "Enter number of seats to book: "

    @staticmethod
    def enter_table_number_to_cancel():
        return "Enter table number to cancel: "

    @staticmethod
    def invalid_numeric_input():
        print("Invalid input. Please enter numeric values.")

    @staticmethod
    def returning_to_dashboard():
        print("Returning to the main dashboard.")

    @staticmethod
    def prompt_return():
        print("\nEnter 'b' to go back to the main dashboard.")

    @staticmethod
    def invalid_input_b():
        print("Invalid input. Please enter 'b' to go back.")

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
    # table_booking.py end
    
    
    # admin_dashboard.py start
    @staticmethod
    def admin_menu():
        print("\n***** Admin Menu *****")
        print("1. Manage Users")
        print("2. Manage Menu")
        print("3. Logout")

    @staticmethod
    def select_option():
        return "Select an option: "

    @staticmethod
    def logging_out():
        print("Logging out...")

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
    #admin dashboard end
    
    #bill_dash start
    @staticmethod
    def billing_management_menu():
        print("\n--- Billing Management ---")
        print("1. Create Bill")
        print("2. Update Bill")
        print("3. Delete Bill")
        print("4. Search Bill by Table Number")
        print("5. View All Bills")
        print("6. Go Back to Dashboard")

    @staticmethod
    def enter_choice():
        return "Enter your choice: "

    @staticmethod
    def returning_to_dashboard():
        print("Returning to the main dashboard.")

    @staticmethod
    def prompt_return():
        print("\nEnter 'b' to go back to the main dashboard.")

    @staticmethod
    def invalid_input_b():
        print("Invalid input. Please enter 'b' to go back.")

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        
    #bill_dash end
    
    #staff_dash start
    @staticmethod
    def staff_menu():
        print("\n***** Staff Menu *****")
        print("1. View Menu")
        print("2. Manage Table Bookings")
        print("3. Manage Orders")
        print("4. Manage Bills")
        print("5. Logout")

    @staticmethod
    def select_option():
        return "Select an option: "

    @staticmethod
    def logging_out():
        print("Logging out.")

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
    #staff dash end
    
    #bill_feature start
    @staticmethod
    def enter_order_id():
        return "Enter the order ID for billing (leave blank if billing by table number): "

    @staticmethod
    def enter_table_number():
        return "Enter the table number for billing: "

    @staticmethod
    def no_orders_found(order_id, table_number):
        if order_id:
            print(f"No orders found for Order ID {order_id}.")
        else:
            print(f"No orders found for Table {table_number}.")

    @staticmethod
    def payment_information():
        print("\n--- Payment Information ---")

    @staticmethod
    def enter_payment_amount(total_amount):
        return f"Total amount is {total_amount}. Enter payment amount: "

    @staticmethod
    def enter_payment_method():
        return "Enter payment method (e.g., cash, online, credit card): "

    @staticmethod
    def enter_mobile_number():
        return "Enter mobile number for the payment: "

    @staticmethod
    def bill_created_successfully():
        print("Bill created and payment processed successfully.")

    @staticmethod
    def error_message(error):
        print(f"Error: {error}")

    @staticmethod
    def enter_bill_id_to_update():
        return "Enter bill ID to update: "

    @staticmethod
    def enter_item_name():
        return "Enter the item name: "

    @staticmethod
    def enter_quantity():
        return "Enter quantity: "

    @staticmethod
    def enter_price():
        return "Enter price: "

    @staticmethod
    def add_another_item():
        return "Add another item? (yes/no): "

    @staticmethod
    def enter_bill_id_to_delete():
        return "Enter bill ID to delete: "

    @staticmethod
    def enter_table_number_for_search():
        return "Enter table number to search for bills: "

    @staticmethod
    def invalid_table_number():
        return "Invalid table number."

    @staticmethod
    def bills_for_table(table_number):
        print(f"\nBills for Table {table_number}:")

    @staticmethod
    def no_bills_found(table_number):
        print(f"No bills found for Table {table_number}.")
    #bill feature end
    
    #manage_bill start
    @staticmethod
    def bill_created_successfully_with_payment():
        print("Bill created successfully with payment details.")

    @staticmethod
    def bill_updated_successfully():
        print("Bill updated successfully.")

    @staticmethod
    def bill_deleted_successfully():
        print("Bill deleted successfully.")

    @staticmethod
    def bill_not_found(bill_id):
        print(f"Bill not found with the given ID: {bill_id}.")

    @staticmethod
    def display_all_bills():
        print("\n" + "=" * 30 + "\n      All Restaurant Bills\n" + "=" * 30)

    @staticmethod
    def separator():
        print("\n" + "=" * 30)

    @staticmethod
    def no_bills_found():
        print("No bills found.")
    # manage_bill end
    
    #menu start
    
    @staticmethod
    @staticmethod
    def error_loading_menu():
        print("Error loading menu data.")

    @staticmethod
    def invalid_meal_type(meal_type=None):
        print(f"Invalid meal type: {meal_type if meal_type else ''}")

    @staticmethod
    def invalid_item_name():
        print("Invalid item name.")

    @staticmethod
    def duplicate_item(name, meal_type):
        print(f"Item '{name}' already exists in {meal_type}.")

    @staticmethod
    def invalid_price():
        print("Invalid price value.")

    @staticmethod
    def item_added(meal_type, item):
        print(f"Added {item} to {meal_type}.")

    @staticmethod
    def item_removed(meal_type, item):
        print(f"Removed {item} from {meal_type}.")

    @staticmethod
    def invalid_index_or_meal_type():
        print("Invalid index or meal type.")
    
    @staticmethod
    def item_already_exists(name):
        print(f"Error: Item '{name}' already exists on the menu.")
    
    @staticmethod
    def invalid_index():
        print("Invalid index.")

    @staticmethod
    def returning_to_dashboard():
        print("Returning to dashboard.")

    @staticmethod
    def menu_management_menu():
        print("\n1. View Menu\n2. Add Item\n3. Remove Item\n4. Return to Dashboard")

    @staticmethod
    def enter_choice():
        return "Enter your choice: "

    @staticmethod
    def enter_meal_type():
        return "Enter meal type: "

    @staticmethod
    def enter_item_name():
        return "Enter item name: "

    @staticmethod
    def enter_item_price():
        return "Enter item full price: "

    @staticmethod
    def prompt_return():
        print("Press 'B' to go back to dashboard.")

    @staticmethod
    def invalid_input_b():
        print("Invalid input. Press 'B' to return.")

    @staticmethod
    def error_message(error):
        print(f"An error occurred: {error}")


    @staticmethod
    def menu_management_menu():
        print("\n--- Menu Management ---")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Remove Menu Item")
        print("4. Go Back to Dashboard")

    @staticmethod
    def enter_choice():
        return "Choose an option: "

    @staticmethod
    def enter_meal_type():
        return "Enter meal type: "

    @staticmethod
    def enter_item_name():
        return "Enter item name: "

    @staticmethod
    def enter_item_price():
        return "Enter item price: "

    @staticmethod
    def enter_item_number_to_remove():
        return "Enter item number to remove: "

    @staticmethod
    def invalid_index():
        print("Invalid index.")

    @staticmethod
    def returning_to_dashboard():
        print("Returning to the main dashboard.")

    @staticmethod
    def prompt_return():
        print("\nEnter 'b' to go back to the main dashboard.")

    @staticmethod
    def invalid_input_b():
        print("Invalid input. Please enter 'b' to go back.")

    @staticmethod
    def invalid_choice():
        print("Invalid choice.")

    @staticmethod
    def error_message(error):
        print(f"Error: {error}")
    #menu end
    
    #manage order start
    @staticmethod
    def order_added_successfully():
        print("Order added successfully.")

    @staticmethod
    def order_updated_successfully(table_number):
        print(f"Order for Table {table_number} updated successfully.")

    @staticmethod
    def order_cancelled_successfully(table_number):
        print(f"Order for Table {table_number} has been cancelled successfully.")

    @staticmethod
    def order_not_found(table_number):
        print(f"No order found for Table {table_number}.")
    # manage order end
    
    #order feature start
    
    @staticmethod
    def enter_customer_name():
        return "Enter customer name: "

    @staticmethod
    def invalid_customer_name():
        return "Invalid customer name."

    @staticmethod
    def enter_order_type():
        return "Is this order 'Eat In' or 'Take Out'? "

    @staticmethod
    def invalid_order_type():
        return "Invalid order type. Please enter 'Eat In' or 'Take Out'."

    @staticmethod
    def enter_items():
        return "Enter items (comma-separated): "

    @staticmethod
    def enter_quantity_for_item(item):
        return f"Enter quantity for {item}: "

    @staticmethod
    def item_not_found(item):
        print(f"Item '{item}' not found in menu.")

    @staticmethod
    def enter_table_number():
        return "Enter table number: "

    @staticmethod
    def invalid_table_number():
        return "Invalid table number."

    @staticmethod
    def enter_seats_required():
        return "Enter the number of seats required: "

    @staticmethod
    def order_added_successfully():
        print("Order added successfully.")

    @staticmethod
    def enter_table_number_to_update():
        return "Enter table number to update order: "

    @staticmethod
    def enter_table_number_to_cancel():
        return "Enter table number to cancel order: "

    @staticmethod
    def enter_table_number_to_search():
        return "Enter table number to search for orders: "

    @staticmethod
    def orders_for_table(table_number):
        print(f"\nOrders for Table {table_number}:")

    @staticmethod
    def no_orders_found(table_number=None):
        if table_number:
            print(f"No orders found for Table {table_number}.")
        else:
            print("No orders found.")

    @staticmethod
    def all_orders():
        print("\nAll Orders:")

    @staticmethod
    def order_management_menu():
        print("\n--- Order Management ---")
        print("1. Add Order")
        print("2. Update Order")
        print("3. Cancel Order")
        print("4. Search Order by Table Number")
        print("5. View All Orders")
        print("6. Go Back to Dashboard")

    @staticmethod
    def prompt_return():
        print("\nEnter 'b' to go back to the main dashboard.")
    
    @staticmethod
    def returning_to_dashboard():
        print("Returning to the main dashboard.")

    @staticmethod
    def invalid_choice():
        print("Invalid choice.")

    @staticmethod
    def error_message(error):
        print(f"Error: {error}")

    @staticmethod
    def invalid_input_b():
        print("Invalid input. Please enter 'b' to go back.")
        
    # order feature end
    
    # payments start
    
    # @staticmethod
    # def enter_payment_amount():
    #     return "Enter payment amount: "

    @staticmethod
    def enter_payment_method():
        return "Enter payment method (e.g., cash, online, credit card): "

    @staticmethod
    def enter_customer_name():
        return "Enter customer name: "

    @staticmethod
    def enter_mobile_number():
        return "Enter mobile number: "

    @staticmethod
    def payment_processed_successfully():
        print("Payment processed successfully!")

    @staticmethod
    def payment_saved_successfully():
        print("Payment data saved successfully.")

    @staticmethod
    def corrupted_payment_file():
        print("Corrupted payment file. Initializing new payment file.")

    @staticmethod
    def no_payment_records():
        print("No payment records found.")

    @staticmethod
    def error_message(error):
        print(f"Error: {error}")
        
    # payments end
    
    @staticmethod
    def enter_portion_size():
        return "Enter portion size (full/half): "
    
    @staticmethod
    def enter_time_slot():
        return "Enter preferred time slot (e.g., 12:00-14:00): "
    
    @staticmethod
    def time_slot_available(time_slot):
        """Display message for available time slots."""
        print(f"Time Slot {time_slot} is available.")

    @staticmethod
    def time_slot_booked(time_slot, customer, seats):
        """Display message for booked time slots."""
        print(f"Time Slot {time_slot} is booked by {customer} for {seats} seats.")

    @staticmethod
    def invalid_time_slot():
        """Display error for invalid time slot."""
        print("Invalid time slot. Please enter a valid time slot.")

    @staticmethod
    def no_table_booking():
        """Display error when no table booking is found."""
        print("No table booking found for the specified customer and time slot.")

    @staticmethod
    def time_slot_already_booked():
        """Display error when time slot is already booked."""
        print("Time slot already booked for the selected table.")