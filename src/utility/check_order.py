
from src.managing_order.order import Order

def check_order(id):
    Order = Order().orders
    for order in Order:
        if(order.id == id):
            return True
    else:
        return False
    

        

        
    

