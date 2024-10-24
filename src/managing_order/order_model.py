
class OrderModel:
    def __init__(self, id, customer_name,table_number, items, quantity, total_amount, order_date):
        self.id = id
        self.customer_name = customer_name
        self.table_number = table_number
        self.items = items
        self.quantity = quantity
        self.total_amount = total_amount
        self.order_date = order_date


    def __str__(self):
        return {
            "id" : {self.id},
            "customer name" : {self.customer_name},
            "table_number"  : {self.table_number},
            "items"  : {self.items},
            "quantity" : {self.quantity},
            "total amount" : {self.total_amount},
            "order date" : {self.order_date}
        }
    

    