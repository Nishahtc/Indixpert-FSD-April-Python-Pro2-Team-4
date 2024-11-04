
class OrderModel:
    def __init__(self, id,  customer_phone_no , customer_name, table_number, items, quantity, price, order_date):
        self.id = id
        self.customer_name = customer_name
        self.customer_phone_no = customer_phone_no
        self.table_number = table_number
        self.items = items
        self.quantity = quantity
        self.price = price
        self.order_date = order_date


    def __str__(self):
        return {
            "id" : {self.id},
            "customer name" : {self.customer_name},
            "customer phone no" : {self.customer_phone_no},
            "table_number"  : {self.table_number},
            "items"  : {self.items},
            "quantity" : {self.quantity},
            "price" : {self.price}, 
            "order date" : {self.order_date}
        }
    

    