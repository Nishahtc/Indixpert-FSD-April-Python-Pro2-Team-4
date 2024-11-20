import json
import os
from src.orders.order_model import OrderModel

ORDER_FILE = "src/database/order.json"

class Order:
    def __init__(self):
        self.orders = self.load_orders()

    def load_orders(self):
        if os.path.exists(ORDER_FILE):
            with open(ORDER_FILE, 'r') as file:
                all_orders = json.load(file)
                return [OrderModel(**order_data) for order_data in all_orders]
        return []

    def save_order(self):
        with open(ORDER_FILE, 'w') as file:
            all_orders = [order.__dict__ for order in self.orders]
            json.dump(all_orders, file, indent=4)
