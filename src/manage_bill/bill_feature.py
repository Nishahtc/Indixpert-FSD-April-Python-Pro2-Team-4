from datetime import datetime
from src.manage_bill.manage_bill import ManageBill
from src.utility.validations import validate_id, validate_mobile_number
from src.orders.order_feature import OrderFeature
from src.payments.payments import Payment, save_payment
from src.menu.menu import Menu
from getpass import getpass
from src.utility.messages import messages
from src.utility.color import bcolors

class BillFeature:
    def __init__(self):
        self.manage_bill = ManageBill()
        self.order_feature = OrderFeature()
        self.menu = Menu()

    def bill_create(self):
        try:
            self.order_feature.orders = self.order_feature.load_orders()

            order_id_input = input(bcolors.colorize("Enter the order ID for billing (leave blank to bill by table number): ",bcolors.TEAL)).strip()

            if order_id_input:
                orders_for_billing = [order for order in self.order_feature.orders if order.id == order_id_input]
            else:
                table_number_input = input(bcolors.colorize("Enter the table number for billing: ",bcolors.TEAL)).strip()
                table_number = int(table_number_input) if table_number_input else None
                orders_for_billing = [
                    order for order in self.order_feature.orders if order.table_number == table_number
                ]

            if not orders_for_billing:
                print(messages.no_orders_found)
                return

            if len(orders_for_billing) > 1:
                print(bcolors.colorize("\nMultiple orders found. Please select one:",bcolors.ORANGE))
                for idx, order in enumerate(orders_for_billing, start=1):
                    print(f"{idx}. Order ID: {order.id}, Customer: {order.customer_name}, Total: {order.total_amount}")
                try:
                    order_choice = int(input(bcolors.colorize("Select the order to bill: ",bcolors.TEAL)).strip())
                    if 1 <= order_choice <= len(orders_for_billing):
                        selected_order = orders_for_billing[order_choice - 1]
                    else:
                        print(messages.invalid_choice)
                        return
                except ValueError:
                    print(messages.invalid_input)
                    return
            else:
                selected_order = orders_for_billing[0]

            item_totals = [
                (selected_order.total_amount / sum(selected_order.quantity)) * qty
                for qty in selected_order.quantity
            ]

            print(bcolors.colorize("\n--- Bill Preview ---",bcolors.LIGHT_GREEN))
            print(bcolors.colorize(f"Customer Name: {selected_order.customer_name}",bcolors.ORANGE))
            print(bcolors.colorize(f"Table Number: {selected_order.table_number}",bcolors.ORANGE))
            print(bcolors.colorize(f"Order Type: {selected_order.order_type}",bcolors.ORANGE))
            print(bcolors.colorize(f"{'Item':<20}{'Quantity':<10}{'Price'}",bcolors.ORANGE))
            print("-" * 40)
            for item, qty, price in zip(selected_order.items, selected_order.quantity, item_totals):
                print(bcolors.colorize(f"{item:<20}{qty:<10}{int(price)}",bcolors.ORANGE))
            print("-" * 40)
            print(bcolors.colorize(f"Total Amount: {int(selected_order.total_amount)}",bcolors.ORANGE))
            print("-" * 40)

            total_amount = selected_order.total_amount
            print(bcolors.colorize(f"\n--- Payment Information ---\nTotal amount to be paid: {total_amount}",bcolors.ORANGE))
            payment_methods = ["Cash", "Card", "UPI"]
            print("\nSelect Payment Method:")
            for idx, method in enumerate(payment_methods, start=1):
                print(bcolors.colorize(f"{idx}. {method}",bcolors.ORANGE))

            while True:
                try:
                    method_choice = int(input("Enter your choice: "))
                    if 1 <= method_choice <= len(payment_methods):
                        payment_method = payment_methods[method_choice - 1]
                        break
                    else:
                        print(messages.invalid_choice)
                except ValueError:
                    print(messages.invalid_input)

            card_number = pin = upi_id = upi_id = None
            if payment_method == "Card":
                while True:
                    card_number = input(bcolors.colorize("Enter your 16-digit card number: ",bcolors.TEAL)).strip()
                    if card_number.isdigit() and len(card_number) == 16 and len(set(card_number)) > 1:
                        break
                    if len(set(card_number)) == 1:
                        print(messages.invalid_card_number)
                    else:
                        print(messages.invalid_card_number)

                while True:
                    pin = getpass(bcolors.colorize("Enter your 4-digit PIN: ",bcolors.TEAL)).strip()
                    if pin.isdigit() and len(pin) == 4 and len(set(pin)) > 1:
                        break
                    if len(set(pin)) == 1:
                        print(messages.invalid_pin)
                    else:
                        print(messages.invalid_pin)
                        
            elif payment_method == "UPI":
                while True:
                    upi_id = input(bcolors.colorize("Enter your UPI ID: ",bcolors.TEAL)).strip().lower()
                    if "@" in upi_id and "." in upi_id.split("@")[-1]:
                        break
                    print(messages.invalid_upi_id)
                
                while True:
                    upi_pin = getpass(bcolors.colorize("Enter your UPI pin: ",bcolors.TEAL)).strip()
                    if upi_pin.isdigit() and len(upi_pin) == 4 and len(set(upi_pin)) > 1:
                        break
                    if len(set(upi_pin)) == 1:
                        print(messages.invalid_upi_pin)
                    else:
                        print(messages.invalid_upi_pin)

            mobile_number = input(bcolors.colorize("Enter customer's mobile number: ",bcolors.TEAL)).strip()
            if not validate_mobile_number(mobile_number):
                print(messages.invalid_mobile_number)
                return

            payment = Payment(
                amount=total_amount,
                method=payment_method,
                customer_name=selected_order.customer_name,
                mobile_number=mobile_number,
                card_number=card_number,
                pin=pin,
            )
            save_payment(payment)

            self.manage_bill.create_bill(
                customer_name=selected_order.customer_name,
                customer_phone_no=mobile_number,
                table_number=selected_order.table_number,
                items=selected_order.items,
                quantities=selected_order.quantity,
                item_totals=item_totals,
                total_amount=total_amount,
                order_type=selected_order.order_type,
                payment_info=payment.to_dict(),
            )

            print(messages.bill_created_success)

            if selected_order.order_type == "eat in":
                self.clear_table_booking(selected_order.table_number, selected_order.customer_name)

        except ValueError as error:
            print(bcolors.colorize(f"Error: {error}",bcolors.RED))

    def clear_table_booking(self, table_number, customer_name):
        booking_system = self.order_feature.table_booking_system
        booking_system.tables = booking_system.load_bookings()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if str(table_number) in booking_system.tables and current_date in booking_system.tables[str(table_number)]:
            bookings = booking_system.tables[str(table_number)][current_date]

            for time_slot, booking in bookings.items():
                if booking and booking["customer"].lower() == customer_name.lower():
                    bookings[time_slot] = None
                    print(bcolors.colorize(f"Booking for Table {table_number} at {time_slot} has been cancelled successfully.",bcolors.LIGHT_GREEN))
                    break

            booking_system.save_bookings()

    def bill_update(self):
        bill_id = validate_id(input(bcolors.colorize("Enter Bill ID to update: ",bcolors.TEAL)).strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return

        updated_data = {
            "customer_name": input(bcolors.colorize("Enter new customer name (leave blank to keep current): ",bcolors.TEAL)).strip() or None,
        }
        updated_data = {key: value for key, value in updated_data.items() if value is not None}

        try:
            updated_bill = self.manage_bill.update_bill(bill_id, updated_data)
            print(bcolors.colorize(f"Updated Bill: {updated_bill}",bcolors.LIGHT_YELLOW))
        except ValueError as e:
            print(e)

    def bill_delete(self):
        bill_id = validate_id(input(bcolors.colorize("Enter Bill ID to delete: ",bcolors.TEAL)).strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return

        self.manage_bill.delete_bill(bill_id)
        print(bcolors.colorize(f"Bill with ID {bill_id} has been deleted successfully.",bcolors.LIGHT_GREEN))

    def search_bill_by_id(self):
        bill_id = validate_id(input(bcolors.colorize("Enter Bill ID to search: ",bcolors.TEAL)).strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return

        bill = self.manage_bill.get_bill(bill_id)
        if bill:
            print(bcolors.colorize(f"\nFound Bill:\n{bill}",bcolors.LIGHT_GREEN))
        else:
            print(bcolors.colorize(f"No bill found with ID: {bill_id}",bcolors.LIGHT_YELLOW))

    def search_all_bills(self):
        all_bills = self.manage_bill.get_all_bills()
        if not all_bills:
            print(messages.no_bills_found)
