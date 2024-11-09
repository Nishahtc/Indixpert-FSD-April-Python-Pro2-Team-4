from src.manage_bill.manage_bill import ManageBill
from src.utility.validations import validate_id, table_number_validate
from src.orders.order_feature import OrderFeature
from src.payments.payments import Payment, save_payment

class BillFeature(ManageBill):
    def __init__(self):
        super().__init__()
        self.order_feature = OrderFeature()

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
                print(f"No orders found for {'Order ID' if order_id_input else f'Table {table_number}'}.")
            
            total_amount = sum(order.total_amount for order in orders_for_billing)
            customer_name = orders_for_billing[0].customer_name
            items = [item for order in orders_for_billing for item in order.items]
            quantities = [qty for order in orders_for_billing for qty in order.quantity]
            
            print("\n--- Payment Information ---")
            amount = float(input(f"Total amount is {total_amount}. Enter payment amount: "))
            method = input("Enter payment method (e.g., cash, online, credit card): ").strip()
            mobile_number = input("Enter mobile number for the payment: ").strip()
            
            payment = Payment(amount, method, customer_name, mobile_number)
            save_payment(payment)
            
            self.create_bill(
                customer_name,
                mobile_number,
                orders_for_billing[0].table_number if orders_for_billing[0].table_number else "Take Out",
                items,
                quantities,
                [order.total_amount for order in orders_for_billing],
                total_amount,
                order_type=orders_for_billing[0].order_type,
                payment_info=payment.to_dict()
            )
            print("Bill created and payment processed successfully.")
            
            if orders_for_billing[0].order_type == "eat in":
                # self.order_feature.table_booking_system.cancel_booking(orders_for_billing[0].table_number)
                table_number = orders_for_billing[0].table_number
                self.order_feature.table_booking_system.cancel_booking(table_number)
                self.order_feature.table_booking_system.save_bookings()
        
        except ValueError as error:
            print(f"Error: {error}")
            
            
    def update(self):
        bill_id = validate_id(input("Enter bill ID to update: "))
        items, quantities, prices = [], [], []

        while True:
            item = input("Enter the item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            items.append(item)
            quantities.append(quantity)
            prices.append(price)

            if input("Add another item? (yes/no): ").strip().lower() != 'yes':
                break

        self.update_bill(bill_id, items, quantities, prices)

    def delete_bill(self):
        bill_id = validate_id(input("Enter bill ID to delete: "))
        self.delete(bill_id)

    def search_bill_by_table(self):
        try:
            table_number = table_number_validate(input("Enter table number to search for bills: "))
            if not table_number:
                raise ValueError("Invalid table number.")
            
            bills_for_table = [bill for bill in self.bills if bill.table_number == table_number]
            if bills_for_table:
                print(f"\nBills for Table {table_number}:")
                for bill in bills_for_table:
                    print(bill)
            else:
                print(f"No bills found for Table {table_number}.")
        except ValueError as error:
            print(error)

    def search_all_bills(self):
        self.get_all_bills()
