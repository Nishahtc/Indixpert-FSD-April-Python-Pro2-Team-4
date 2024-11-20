from src.utility.color import bcolors
class BillModel:
    def __init__(self, bill_id, customer_name, customer_phone_no, table_number, items, quantities, item_totals, total_amount, order_type=None, payment_info=None):
        self.bill_id = bill_id
        self.customer_name = customer_name
        self.customer_phone_no = customer_phone_no
        self.table_number = table_number
        self.items = items
        self.quantities = quantities
        self.item_totals = item_totals
        self.total_amount = total_amount
        self.order_type = order_type
        self.payment_info = payment_info

    def __str__(self):
        output = "\n" + "=" * 40
        output += bcolors.colorize(f"\n{'Restaurant Bill':^40}",bcolors.LIGHT_GREEN)
        output += "\n" + "=" * 40
        output += bcolors.colorize(f"\nBill ID      : {self.bill_id}",bcolors.ORANGE)
        output += bcolors.colorize(f"\nCustomer Name: {self.customer_name}",bcolors.ORANGE)
        output += bcolors.colorize(f"\nTable Number : {self.table_number}",bcolors.ORANGE)
        output += bcolors.colorize(f"\nOrder Type   : {self.order_type}",bcolors.ORANGE)
        output += "\n" + "-" * 40

        output += bcolors.colorize(f"\n{'Item':<25}{'Qty':<5}{'Total':>10}",bcolors.ORANGE)
        output += "\n" + "-" * 40

        for item, qty, item_total in zip(self.items, self.quantities, self.item_totals):
            output += bcolors.colorize(f"\n{item:<25}{qty:<5}{int(item_total):>10}",bcolors.ORANGE)

        output += "\n" + "-" * 40
        output += bcolors.colorize(f"\n{'Total Amount':<30}{int(self.total_amount):>10}",bcolors.ORANGE)

        if self.payment_info:
            output += "\n" + "-" * 40
            output += bcolors.colorize(f"\nPayment Method: {self.payment_info['method']}",bcolors.ORANGE)
            output += bcolors.colorize(f"\nAmount Paid   : {int(self.payment_info['amount'])}",bcolors.ORANGE)
            output += bcolors.colorize(f"\nMobile Number : {self.payment_info['mobile_number']}",bcolors.ORANGE)
            output += "\n" + "=" * 40
        else:
            output += bcolors.colorize(f"\n{'Payment':<30}Not completed",bcolors.ORANGE)
            output += "\n" + "=" * 30

        return output