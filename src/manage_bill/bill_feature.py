import uuid
from src.manage_bill.manage_bill import ManageBill
from src.utility.validations import validate_id, table_number_validate
from src.orders.order_feature import OrderFeature
from src.payments.payments import Payment, save_payment
from src.utility.messages import Messages

class BillFeature(ManageBill):
    def __init__(self):
        super().__init__()
        self.order_feature = OrderFeature()

    def bill_create(self):
        try:
            self.order_feature.orders = self.order_feature.load_orders()

            order_id_input = input(Messages.enter_order_id()).strip()

            if order_id_input:
                orders_for_billing = [order for order in self.order_feature.orders if order.id == order_id_input]
            else:
                table_number_input = input(Messages.enter_table_number()).strip()
                table_number = int(table_number_input) if table_number_input else None
                orders_for_billing = [order for order in self.order_feature.orders if order.table_number == table_number]

            if not orders_for_billing:
                Messages.no_orders_found(order_id_input, table_number)
                return

            total_amount = 0
            items = []
            quantities = []
            item_prices = []

            for order in orders_for_billing:
                for item, qty in zip(order.items, order.quantity):
                    portion_size = input(f"Enter portion size for {item} (full/half): ").strip().lower()
                    if portion_size not in ['full', 'half']:
                        Messages.invalid_choice()
                        continue
                    price = self.order_feature.menu.get_item_price(item, portion_size)
                    if price is None:
                        Messages.item_not_found(item)
                        continue
                    items.append(item)
                    quantities.append(qty)
                    item_prices.append(price)
                    total_amount += price * qty

            customer_name = orders_for_billing[0].customer_name

            Messages.payment_information()
            amount = float(input(Messages.enter_payment_amount(total_amount)))
            method = input(Messages.enter_payment_method()).strip()
            mobile_number = input(Messages.enter_mobile_number()).strip()

            payment = Payment(amount, method, customer_name, mobile_number)
            save_payment(payment)

            self.create_bill(
                customer_name,
                mobile_number,
                orders_for_billing[0].table_number if orders_for_billing[0].table_number else "Take Out",
                items,
                quantities,
                item_prices,
                total_amount,
                order_type=orders_for_billing[0].order_type,
                payment_info=payment.to_dict()
            )
            Messages.bill_created_successfully()

            if orders_for_billing[0].order_type == "eat in":
                table_number = orders_for_billing[0].table_number
                
                booking_system = self.order_feature.table_booking_system
                booking_system.tables = booking_system.load_bookings()
                
                time_slot = None
                customer_name = orders_for_billing[0].customer_name
                for slot, booking in booking_system.tables[str(table_number)]['bookings'].items():
                    if booking and booking['customer'].lower() == customer_name.lower():
                        time_slot = slot
                        break
                
                if time_slot:
                    booking_system.cancel_booking(table_number, time_slot)
                    booking_system.save_bookings()
                    Messages.booking_cancelled(table_number)
                else:
                    Messages.no_booking_found()
                    
        except ValueError as error:
            Messages.error_message(error)

    def update(self):
        bill_id = validate_id(input(Messages.enter_bill_id_to_update()))
        items, quantities, prices = [], [], []

        while True:
            item = input(Messages.enter_item_name())
            quantity = int(input(Messages.enter_quantity()))
            portion_size = input(f"Enter portion size for {item} (full/half): ").strip().lower()
            if portion_size not in ['full', 'half']:
                Messages.invalid_choice()
                continue

            price = self.order_feature.menu.get_item_price(item, portion_size)
            if price is None:
                Messages.item_not_found(item)
                continue

            items.append(item)
            quantities.append(quantity)
            prices.append(price)

            if input(Messages.add_another_item()).strip().lower() != 'yes':
                break

        self.update_bill(bill_id, items, quantities, prices)

    def delete_bill(self):
        bill_id = validate_id(input(Messages.enter_bill_id_to_delete()))
        self.delete(bill_id)

    def search_bill_by_table(self):
        try:
            table_number = table_number_validate(input(Messages.enter_table_number_for_search()))
            if not table_number:
                raise ValueError(Messages.invalid_table_number())

            bills_for_table = [bill for bill in self.bills if bill.table_number == table_number]
            if bills_for_table:
                Messages.bills_for_table(table_number)
                for bill in bills_for_table:
                    print(bill)
            else:
                Messages.no_bills_found(table_number)
        except ValueError as error:
            Messages.error_message(error)

    def search_all_bills(self):
        self.get_all_bills()
