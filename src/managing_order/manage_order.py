import uuid
from datetime import datetime
from src.managing_order.order_model import OrderModel
from src.managing_order.order import Order
from src.

class ManageOrder(Order):
    def add_order(self, id, customer_name, table_number,items, quantity, total_amount, order_date):
        id = str(uuid.uuid4())[:4]
        order_date = datetime.now()
        new_order = OrderModel(id, customer_name, table_number,items, quantity, total_amount, order_date )
        self.orders.append(new_order)
        self.save_order()
        print("Your order added succesfully")

    def update_order(self, id, customer_name, items, quantity, table_number ):
        if(user.role == ""):#...what is here
            for order in self.orders:
                if(order.id == id):
                    order.customer_name = customer_name
                    order.items = items
                    order.quantity = quantity
                    order.table_number = table_number
                    self.save_order()
                    print("updated order succesfully")
                    break 
            
            else:
                print("order not found with id")

    def cancel_order(self, id):
        if(user.role == ""): #..
            for order in self.orders:
                if(order.id == id ):
                    self.orders.remove(order)
                    self.save_order()
                    print("order has been cancelled succesfully")
                    break
        else:
                print("your order not found")

            
    def get_order(self, id):
        for order in self.orders:
             if(order.id == id):
                print(f"order id - {id}: order - {order.items} ")
                break
             
        else:
            print("order not found")

    
    def get_all_order(self):
        print(f"{'ID':<10} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
        print('-' * 120)  # Line separator
        if(len(self.orders))>0:
            for order in self.orders:
                print(f"{order.id:<10} {order.customer_name:<20} {order.table_number:<15} {', '.join(order.items):<30} {order.quantity:<10} {order.total_amount:<15} {order.order_date.strftime('%Y-%m-%d %H:%M:%S'):<20}")

        else:
            print("no order found")       
               
