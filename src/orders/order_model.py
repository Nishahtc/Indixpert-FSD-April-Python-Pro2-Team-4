from datetime import datetime
from src.utility.color import bcolors

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
        output += bcolors.colorize(f"\n{'Order Summary':^30}",bcolors.LIGHT_GREEN)
        output += "\n" + "=" * 30
        output += bcolors.colorize(f"\nOrder ID      : {self.id}",bcolors.CYAN)
        output += bcolors.colorize(f"\nCustomer Name : {self.customer_name}",bcolors.CYAN)
        output += bcolors.colorize(f"\nTable Number  : {self.table_number}",bcolors.CYAN)
        output += bcolors.colorize(f"\nOrder Type    : {self.order_type}",bcolors.CYAN)
        output += bcolors.colorize(f"\nOrder Date    : {self.order_date}",bcolors.CYAN)
        output += "\n" + "-" * 30

        output += bcolors.colorize(f"\n{'Item':<15}{'Qty':<5}{'Total'}",bcolors.CYAN)
        output += "\n" + "-" * 30

        for item, qty in zip(self.items, self.quantity):
            item_total = qty * self.total_amount // sum(self.quantity)
            output += bcolors.colorize(f"\n{item:<15}{qty:<5}{item_total:.2f}",bcolors.CYAN)

        output += "\n" + "-" * 30
        output += bcolors.colorize(f"\n{'Total Amount':<20}{self.total_amount:.2f}",bcolors.CYAN)
        output += "\n" + "=" * 30

        return output
