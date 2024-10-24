import json
import os
from src.managing_order.order_model import OrderModel
ORDER_FILE = "src/database/order.json"

class Order:
    def __init__(self):
        self.orders = self.load_orders()

    def load_orders(self):
        if os.path.exists(ORDER_FILE):
            with open(ORDER_FILE,'r') as file:
                all_order = json.load(file)
                return [OrderModel(**oi) for oi in all_order]
        else:
            return []
        
    def save_order(self):
        with open(ORDER_FILE,'w') as file:
            all_order = [oi.__dic__ for oi in self.orders]
            json.dump(all_order, file, indent=4)


            


