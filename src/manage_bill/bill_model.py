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
        output = "\n" + "=" * 30
        output += f"\n{'Restaurant Bill':^30}"
        output += "\n" + "=" * 30
        output += f"\nBill ID      : {self.bill_id}"
        output += f"\nCustomer Name: {self.customer_name}"
        output += f"\nTable Number : {self.table_number}"
        output += f"\nOrder Type   : {self.order_type}"
        output += "\n" + "-" * 30

        output += f"\n{'Item':<15}{'Qty':<5}{'Total'}"
        output += "\n" + "-" * 30

        for item, qty, item_total in zip(self.items, self.quantities, self.item_totals):
            output += f"\n{item:<15}{qty:<5}{item_total:.2f}"

        output += "\n" + "-" * 30
        output += f"\n{'Total Amount':<20}{self.total_amount:.2f}"

        if self.payment_info:
            output += "\n" + "-" * 30
            output += f"\nPayment Method: {self.payment_info['method']}"
            output += f"\nAmount Paid   : {self.payment_info['amount']:.2f}"
            output += f"\nMobile Number : {self.payment_info['mobile_number']}"
            output += "\n" + "=" * 30
        else:
            output += f"\n{'Payment':<20}Not completed"
            output += "\n" + "=" * 30

        return output