import uuid
from datetime import datetime
from src.managing_order.order_model import OrderModel
from src.managing_order.order import Order

class ManageOrder(Order):
    def add_order(self, id, customer_name, table_number,items, quantity, total_amount, order_date):
        id = str(uuid.uuid4())[:4]
        order_date = datetime.now()
        new_order = OrderModel(id, customer_name, table_number,items, quantity, total_amount, order_date )
        self.orders.append(new_order)
        self.save_order()
        print("Your order added succesfully")

    def update_order(self, id, ):
        for order in self.orders:
            if order.id == id:
                order.id = id
                self.save_order()
                print("Your order updated successfully")
                break
        else:
            print("Your orderd id not match")

    def cancel_order(self,id,items):
        





   

        

