if __name__ == "__main__":  # Corrected the main check
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