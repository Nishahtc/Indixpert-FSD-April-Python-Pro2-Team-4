import uuid
from datetime import datetime
from src.managing_order.order_model import OrderModel
from src.managing_order.order import Order
from src


class ManageOrder(Order):
        def add_order(self, id, customer_name, customer_phone_no, table_number, items, quantity, price, order_date):
            id = str(uuid.uuid4())[:6]
            order_date = datetime.now()
            new_order = OrderModel(id, customer_name, customer_phone_no, table_number,items, quantity, price, order_date )
            self.orders.append(new_order)
            self.save_order()
            print("Your order added succesfully")

        def update_order(self, id, items, quantity, price, order_date ):
            order_date = datetime.now()
            for order in self.orders:
                if(order.id == id):
                    order.items = items
                    order.quantity = quantity
                    order.price = price
                    print("Order updated successfully")
                    break

            else:
                print(f"Order not found with id {id}")


        def cancel_order(self, id):
            for order in self.orders:
                if(order.id == id):
                    self.orders.remove(order)
                    self.save_order()
                    print("Order deleted successfully")


        def get_order(self, id):
            for order in self.orders:
                if(order.id == id):
                    print(f"{'ID':<10} {'customer phone_no' :<15} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
                    print(f'-'* 135)
                    print(f"{order.id:<10}  {order.customer_phone_no:<15} {order.customer_name:<20} {order.table_number:<15} {order.items:<30} {order.quantity:<10} {order.price:<15} {order.order_date.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                    break
            
            else:
                print("Order not found")


        def get_all_order(self):
            print(f"{'ID':<10} {'customer phone_no' :<15} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
            print(f'-'* 135)
            if(len(self.orders))>0:
                for order in self.orders:
                    print(f"{order.id:<10}  {order.customer_phone_no:<15} {order.customer_name:<20} {order.table_number:<15} {order.items:<30} {order.quantity:<10} {order.price:<15} {order.order_date.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                    print('*'*135)

            else:
                print("Order  not found")
            




