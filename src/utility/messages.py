class Messages:
    def __init__(self):
        
     
        def error_message(text):
            return f"\033[91m{text}\033[0m"  
        
        def info_message(text):
            return f"\033[93m{text}\033[0m"  
        
  # General error messages
        self.invalid_input = error_message("Invalid input. Please enter a valid value.")
        self.invalid_choice = error_message("Invalid choice. Please try again.")
        self.action_canceled = error_message("Action canceled.")
        self.operation_failed = error_message("Operation failed. Please try again.")
        self.exiting_system = error_message("Exiting the system.")
        self.data_load_error = error_message("Error loading data. Starting with an empty list.")
        self.data_save_error = error_message("Error saving data.")
        self.log_out = error_message("Logging out...")
        self.returning_dashboard = info_message("Returning to the main dashboard.")
        self.no_items_selected = error_message("No items selected. Order cancelled.")

        # Authentication error messages
        self.invalid_choice = error_message( "Invalid choice. Please try again.")
        self.data_load_error = error_message("Error loading user data.")
        self.data_save_error = error_message("Error saving user data.")
        self.invalid_credentials = error_message ("Invalid username or password.")
        self.username_exists = info_message ("This username is already taken.")
        self.invalid_email = error_message("Invalid email format.")
        self.invalid_mobile_number = error_message("Invalid mobile number format.")
        self.user_signup_success = info_message("User registered successfully!")
        self.no_registered_users = info_message("No users are currently registered.")
        self.user_deleted = info_message( "User deleted successfully.")
        self.user_not_found = info_message("User not found.")
        self.exiting_system = info_message("Exiting the system. Goodbye!")

        # Booking messages
        self.invalid_table_number = error_message("Invalid table number. Please choose a valid table.")
        self.table_already_booked = error_message("This table is already booked for the selected time slot.")
        self.no_available_slots = error_message("No available time slots for the selected table.")
        self.booking_not_found = error_message("No bookings found for the given table or date.")
        self.no_bookings = info_message("No bookings for the next 7 days.")
        self.booking_failed = error_message("Booking failed. Order cannot proceed.")

        # Menu management messages
        self.menu_empty = info_message("No items available in the menu.")
        self.item_exists = error_message("This item already exists in the menu.")
        self.item_not_found = error_message("Item not found in the menu.")
        self.invalid_meal_type = error_message("Invalid meal type selected. Please choose a valid meal type.")
        self.invalid_price_format = error_message("Invalid price format. Please enter a numeric value.")
        self.menu_add_success = info_message("Item added to menu successfully.")
        self.menu_remove_success = info_message("Item removed from menu successfully.")
        self.menu_save_error = error_message("Error saving menu data.")

        # Order management messages
        self.no_orders_found = info_message("No orders found.")
        self.order_add_success = info_message("Order added successfully.")
        self.order_update_success = info_message("Order updated successfully.")
        self.order_cancel_success = info_message("Order canceled successfully.")
        self.order_not_found = error_message("Order not found with the given ID.")
        self.invalid_order_id = error_message("Invalid order ID. Please enter a valid order ID.")
        self.invalid_table_for_order = error_message("Invalid table number for the order.")
        self.order_save_error = error_message("Error saving order data.")
        self.order_load_error = error_message("Error loading orders data.")

        # Billing messages
        self.bill_not_found = error_message("Bill not found with the given ID.")
        self.no_bills_found = info_message("No bills found.")
        self.bill_created_success = info_message("Bill created successfully.")
        self.bill_update_success = info_message("Bill updated successfully.")
        self.bill_deleted_success = info_message("Bill deleted successfully.")
        self.invalid_bill_id = error_message("Invalid bill ID. Please enter a valid bill ID.")
        self.bill_save_error = error_message("Error saving bill data.")
        self.bill_load_error = error_message("Error loading bill data.")

        # Payment messages
        self.invalid_payment_method = error_message("Invalid payment method selected.")
        self.payment_saved_success = info_message("Payment data saved successfully.")
        self.no_payment_records = info_message("No payment records found.")
        self.payment_success = info_message("Payment processed successfully.")
        self.payment_failed = error_message("Payment failed. Please try again.")
        self.invalid_card_number = error_message("Invalid credit card number.")
        self.invalid_pin = error_message("Invalid PIN.")
        self.invalid_mobile_number_for_payment = error_message("Invalid mobile number. It should be exactly 10 digits.")
        self.payment_save_error = error_message("Error saving payment information.")
        self.corrupted_payment_file = error_message("Corrupted payment file. Initializing new payment file.")
        self.invalid_upi_id = error_message("Invalid UPI ID.")
        self.invalid_upi_pin = error_message("Invalid UPI pin.")

        # Validation error messages
        self.customer_name_invalid = error_message("Invalid customer name. Only alphabetic characters are allowed.")
        self.quantity_invalid = error_message("Invalid quantity. Please enter a positive integer.")
        self.portion_size_invalid = error_message("Invalid portion size. Please enter 'full' or 'half'.")
        self.meal_type_invalid = error_message("Invalid meal type selected.")
        self.date_format_invalid = error_message("Invalid date format. Please use YYYY-MM-DD.")
        self.time_format_invalid = error_message("Invalid time format. Please use HH:MM.")
        self.prompt_return = info_message("Enter 'b' to go back to the main dashboard.")   
        self.invalid_booking_date = error_message("Invalid booking date. Please select a future date.")
        self.invalid_booking_time = error_message("Invalid booking time. Please select a valid time slot.")
        self.booking_cancel_success = info_message("Booking canceled successfully.")
        self.booking_save_error = error_message("Error saving booking data.")
        self.table_booking_success = info_message("Table booked successfully.")
        self.booking_save_success = info_message("Booking data saved successfully.")

messages = Messages()
