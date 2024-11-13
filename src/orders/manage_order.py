import uuid
from datetime import datetime
from src.orders.order_model import OrderModel
from src.orders.order import Order
from src.utility.messages import Messages

class ManageOrder(Order):
    def add_order(self, customer_name, table_number, items, quantity, total_amount):
        order_id = str(uuid.uuid4())[:6]
        order_date = datetime.now()
        new_order = OrderModel(order_id, customer_name, table_number, items, quantity, total_amount, order_date)
        self.orders.append(new_order)
        self.save_order()
        Messages.order_added_successfully()

    def update_order(self, table_number, customer_name, items, quantity, total_amount):
        for order in self.orders:
            if order.table_number == table_number:
                order.customer_name = customer_name
                order.items = items
                order.quantity = quantity
                order.total_amount = total_amount
                self.save_order()
                Messages.order_updated_successfully(table_number)
                return
        Messages.order_not_found(table_number)

    def cancel_order(self, table_number):
        for order in self.orders:
            if order.table_number == table_number:
                self.orders.remove(order)
                self.save_order()
                Messages.order_cancelled_successfully(table_number)
                return
        Messages.order_not_found(table_number)
