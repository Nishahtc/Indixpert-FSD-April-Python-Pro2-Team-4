import uuid
from datetime import datetime
from src.orders.manage_order import ManageOrder
from src.orders.order_model import OrderModel
from src.utility.validations import customer_name_validate, table_number_validate
from src.menu.menu import Menu
from src.booking.table_booking import TableBookingSystem
from src.utility.messages import Messages


class OrderFeature(ManageOrder):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        self.table_booking_system = TableBookingSystem()

    def order(self):
        try:
            customer_name = customer_name_validate(input(Messages.enter_customer_name()))
            if not customer_name:
                raise ValueError(Messages.invalid_customer_name())

            order_type = input(Messages.enter_order_type()).strip().lower()
            if order_type not in ("eat in", "take out"):
                raise ValueError(Messages.invalid_order_type())
            
            table_number = None
            
            if order_type == "eat in":
                table_number = table_number_validate(input(Messages.enter_table_number()))
                if not table_number:
                    raise ValueError(Messages.invalid_table_number())

                time_slot = input(Messages.enter_time_slot()).strip()
                if not time_slot or time_slot not in self.table_booking_system.TIME_SLOTS:
                    raise ValueError(Messages.invalid_time_slot())

                if not self.table_booking_system.is_table_booked(table_number, customer_name, time_slot):
                    Messages.no_table_booking()
                    print("Please book a table first before placing an 'Eat In' order.")
                    return

            items = input(Messages.enter_items()).split(',')
            items = [item.strip() for item in items if item.strip()]

            total_amount = 0
            quantities = []
            for item in items:
                quantity = int(input(Messages.enter_quantity_for_item(item)))
                portion_size = input(Messages.enter_portion_size()).strip().lower()
                if portion_size not in ['full', 'half']:
                    Messages.invalid_choice()
                    continue
                price = self.menu.get_item_price(item, portion_size)
                if price is None:
                    Messages.item_not_found(item)
                    continue
                quantities.append(quantity)
                total_amount += price * quantity

            self.add_order(customer_name, table_number, items, quantities, total_amount, order_type)
        except ValueError as error:
            Messages.error_message(error)

    def add_order(self, customer_name, table_number, items, quantities, total_amount, order_type):
        order_id = str(uuid.uuid4())[:6]
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if order_type == "take out":
            table_number = None

        new_order = OrderModel(
            id=order_id,
            customer_name=customer_name,
            table_number=table_number,
            items=items,
            quantity=quantities,
            total_amount=total_amount,
            order_date=order_date,
            order_type=order_type
        )
        self.orders.append(new_order)
        self.save_order()
        Messages.order_added_successfully()

    def update_item(self):
        try:
            table_number = table_number_validate(input(Messages.enter_table_number_to_update()))
            if not table_number:
                raise ValueError(Messages.invalid_table_number())

            customer_name = customer_name_validate(input(Messages.enter_customer_name()))
            items = input(Messages.enter_items()).split(',')
            items = [item.strip() for item in items]

            total_amount = 0
            quantities = []
            for item in items:
                quantity = int(input(Messages.enter_quantity_for_item(item)))
                portion_size = input(Messages.enter_portion_size()).strip().lower()
                if portion_size not in ['full', 'half']:
                    Messages.invalid_choice()
                    continue
                price = self.menu.get_item_price(item, portion_size)
                if price is None:
                    Messages.item_not_found(item)
                    continue
                quantities.append(quantity)
                total_amount += price * quantity

            self.update_order(table_number, customer_name, items, quantities, total_amount)
        except ValueError as error:
            Messages.error_message(error)

    def cancel_item(self):
        try:
            table_number = table_number_validate(input(Messages.enter_table_number_to_cancel()))
            if not table_number:
                raise ValueError(Messages.invalid_table_number())
            self.cancel_order(table_number)
        except ValueError as error:
            Messages.error_message(error)

    def search_order_by_table(self):
        try:
            table_number = table_number_validate(input(Messages.enter_table_number_to_search()))
            if not table_number:
                raise ValueError(Messages.invalid_table_number())

            found_orders = [order for order in self.orders if order.table_number == table_number]
            if found_orders:
                Messages.orders_for_table(table_number)
                for order in found_orders:
                    print(order)
            else:
                Messages.no_orders_found(table_number)
        except ValueError as error:
            Messages.error_message(error)

    def search_all_orders(self):
        if self.orders:
            Messages.all_orders()
            for order in self.orders:
                print(order)
        else:
            Messages.no_orders_found()

    def manage_orders(self):
        while True:
            Messages.order_management_menu()
            choice = input(Messages.enter_choice()).strip()

            if choice == '1':
                self.order()
            elif choice == '2':
                self.update_item()
            elif choice == '3':
                self.cancel_item()
            elif choice == '4':
                self.search_order_by_table()
                self.prompt_return_to_dashboard()
            elif choice == '5':
                self.search_all_orders()
                self.prompt_return_to_dashboard()
            elif choice == '6':
                Messages.returning_to_dashboard()
                break
            else:
                Messages.invalid_choice()

    def prompt_return_to_dashboard(self):
        while True:
            Messages.prompt_return()
            user_input = input(Messages.enter_choice()).strip().lower()
            if user_input == 'b':
                break
            else:
                Messages.invalid_input_b()
