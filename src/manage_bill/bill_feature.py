from datetime import datetime
from src.manage_bill.manage_bill import ManageBill
from src.utility.validations import validate_id, validate_mobile_number
from src.orders.order_feature import OrderFeature
from src.payments.payments import Payment, save_payment
from src.menu.menu import Menu
from getpass import getpass
from src.utility.messages import messages

class BillFeature(ManageBill):
    def __init__(self):
        super().__init__()
        self.order_feature = OrderFeature()
        self.menu = Menu()

    def bill_create(self):
        try:
            self.order_feature.orders = self.order_feature.load_orders()
            order_id_input = input("Enter the order ID for billing (leave blank if billing by table number): ").strip()
            
            if order_id_input:
                orders_for_billing = [order for order in self.order_feature.orders if order.id == order_id_input]
            else:
                table_number_input = input("Enter the table number for billing: ").strip()
                table_number = int(table_number_input) if table_number_input else None
                orders_for_billing = [order for order in self.order_feature.orders if order.table_number == table_number]
                
            if not orders_for_billing:
                print(messages.no_orders_found)
                return
            
            if len(orders_for_billing) > 1:
                print("\nMultiple orders found for Table", table_number)
                for idx, order in enumerate(orders_for_billing, start=1):
                    print(f"{idx}. Order ID: {order.id}, Customer: {order.customer_name}, Total: {order.total_amount}")
                    
                try:
                    order_choice = int(input("Select the order to bill: ").strip())
                    if order_choice < 1 or order_choice > len(orders_for_billing):
                        print(messages.invalid_choice)
                        return
                    
                    orders_for_billing = [orders_for_billing[order_choice - 1]]
                except ValueError:
                    print(messages.invalid_input)
                    return
            
            selected_order = orders_for_billing[0]
            items = selected_order.items
            quantities = selected_order.quantity
            total_amount = selected_order.total_amount
            item_prices = []
            
            for item, qty in zip(items, quantities):
                full_price = self.order_feature.menu.get_item_price(item, 'full')
                half_price = self.order_feature.menu.get_item_price(item, 'half')
                
                if full_price * qty == total_amount / len(items):
                    item_prices.append(full_price)
                else:
                    item_prices.append(half_price)
            
            customer_name = selected_order.customer_name
            
            print("\n--- Payment Information ---")
            print(f"Total amount to be paid: {total_amount}")
            payment_methods = ["Cash", "Card"]
            print("\nSelect Payment Method:")
            for idx, method in enumerate(payment_methods, start=1):
                print(f"{idx}. {method}")
            
            while True:
                try:
                    method_choice = int(input("Enter your choice: ").strip())
                    if 1 <= method_choice <= len(payment_methods):
                        method = payment_methods[method_choice - 1]
                        break
                    else:
                        print(messages.invalid_choice)
                except ValueError:
                    print(messages.invalid_input)
            
            credit_card_number = None
            pin = None
            if method == "Card":
                while True:
                    credit_card_number = input("Enter your 16-digit credit card number: ").strip()
                    if credit_card_number.isdigit() and len(credit_card_number) == 16:
                        break
                    else:
                        print(messages.invalid_card_number)
                        
                while True:
                    pin = getpass("Enter your 4-digit PIN: ").strip()
                    if pin.isdigit() and len(pin) == 4:
                        break
                    else:
                        print(messages.invalid_pin)
                        
            while True:
                mobile_number = input("enter mobile number: ").strip()
                if validate_mobile_number(mobile_number):
                    break
                else:
                    print(messages.invalid_mobile_number)

            payment = Payment(amount=total_amount, method=method, customer_name=selected_order.customer_name, 
                  mobile_number=mobile_number, card_number=credit_card_number, pin=pin)
            save_payment(payment)
            
            self.create_bill(
                customer_name,
                mobile_number,
                selected_order.table_number if selected_order.table_number else "Take Out",
                items,
                quantities,
                item_prices,
                total_amount,
                order_type=selected_order.order_type,
                payment_info=payment.to_dict()
            )
            print(messages.bill_created_success)
            
            if selected_order.order_type == "eat in":
                self.clear_table_booking(selected_order.table_number, customer_name)
        
        except ValueError as error:
            print(f"Error: {error}")
    
    def clear_table_booking(self, table_number, customer_name):
        booking_system = self.order_feature.table_booking_system
        booking_system.tables = booking_system.load_bookings()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if str(table_number) in booking_system.tables and current_date in booking_system.tables[str(table_number)]:
            bookings = booking_system.tables[str(table_number)][current_date]
            
            for time_slot, booking in bookings.items():
                if booking and booking['customer'].lower() == customer_name.lower():
                    bookings[time_slot] = None
                    print(f"Booking for Table {table_number} at {time_slot} has been cancelled successfully.")
                    break
            
            booking_system.save_bookings()

    def update(self):
        bill_id = validate_id(input("Enter bill ID to update: ").strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return
        
        bill_id = bill_id.lower()
        
        found_bill = next((bill for bill in self.bills if bill.bill_id.lower() == bill_id), None)
        if not found_bill:
            print(f"Bill not found with the given ID: {bill_id.upper()}")
            return
        
        print(f"\nUpdating Bill ID: {bill_id.upper()} - Customer: {found_bill.customer_name}")
        items, quantities, prices = found_bill.items, found_bill.quantities, found_bill.item_totals
        
        
        while True:
            print("\n--- Update Bill Items ---")
            item = input("Enter the item name (leave blank to stop): ").strip()
            if not item:
                break
            
            if item not in items:
                print(f"Item '{item}' not found in the existing bill.")
                continue
            
            index = items.index(item)
            
            quantity_input = input(f"Enter new quantity for '{item}' (leave blank to keep {quantities[index]}): ").strip()
            if quantity_input:
                try:
                    quantities[index] = int(quantity_input)
                except ValueError:
                    print(messages.invalid_input)
                    continue
            
            portion_size = input(f"Enter new portion size for '{item}' (full/half, leave blank to keep current): ").strip().lower()
            if portion_size in ['full', 'half']:
                price = self.menu.get_item_price(item, portion_size)
                if price is not None:
                    prices[index] = price
                else:
                    print(f"Item '{item}' not found in the menu.")
                    continue
            else:
                print("Keeping existing portion size.")
            
            if input("Update another item? (yes/no): ").strip().lower() != 'yes':
                break
        
        found_bill.total_amount = sum(qty * price for qty, price in zip(quantities, prices))
        found_bill.items = items
        found_bill.quantities = quantities
        found_bill.item_totals = prices
        
        self.save_bills()
        print(f"\nBill ID {bill_id.upper()} updated successfully!")
            
    def delete_bill(self):
        bill_id = validate_id(input("Enter bill ID to delete: ").strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return
        
        bill_id = bill_id.lower()
        
        found_bill = next((bill for bill in self.bills if bill.bill_id.lower() == bill_id), None)
        if not found_bill:
            print(f"Bill not found with the given ID: {bill_id.upper()}")
            return
        
        self.bills.remove(found_bill)
        self.save_bills()
        print(f"Bill ID {bill_id.upper()} deleted successfully.")

    def search_bill_by_id(self):
        bill_id = validate_id(input("Enter bill ID to search: ").strip())
        if not bill_id:
            print(messages.invalid_bill_id)
            return
        
        bill_id = bill_id.lower()
        
        found_bill = next((bill for bill in self.bills if bill.bill_id == bill_id), None)
        
        if found_bill:
            print(f"\nFound Bill:\n{found_bill}")
        else:
            print(f"No bill found with ID: {bill_id}")

    def search_all_bills(self):
        self.get_all_bills()
