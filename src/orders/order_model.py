from datetime import datetime

class OrderModel:
    def __init__(self, id, customer_name, table_number, items, quantity, total_amount, order_date=None, order_type=None):
        self.id = id
        self.customer_name = customer_name
        self.table_number = table_number
        self.items = items
        self.quantity = quantity
        self.total_amount = total_amount
        
        if isinstance(order_date, str):
            self.order_date = order_date
        else:
            self.order_date = (order_date or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        
        self.order_type = order_type

    def __str__(self):
        output = "\n" + "=" * 30
        output += f"\n{'Order Summary':^30}"
        output += "\n" + "=" * 30
        output += f"\nOrder ID      : {self.id}"
        output += f"\nCustomer Name : {self.customer_name}"
        output += f"\nTable Number  : {self.table_number}"
        output += f"\nOrder Type    : {self.order_type}"
        output += f"\nOrder Date    : {self.order_date}"
        output += "\n" + "-" * 30

        output += f"\n{'Item':<15}{'Qty':<5}{'Total'}"
        output += "\n" + "-" * 30

        for item, qty in zip(self.items, self.quantity):
            item_total = qty * self.total_amount // sum(self.quantity)
            output += f"\n{item:<15}{qty:<5}{item_total:.2f}"

        output += "\n" + "-" * 30
        output += f"\n{'Total Amount':<20}{self.total_amount:.2f}"
        output += "\n" + "=" * 30

        return output
