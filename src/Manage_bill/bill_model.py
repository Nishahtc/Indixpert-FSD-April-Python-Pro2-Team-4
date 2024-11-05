
class BillModel:
    def __init__(
            self,
            bill_id,
            customer_phone_no,
            customer_name,
            items,
            quantity,
            table_number,
            price,
            total_amount,
            date_time
    ):
        self.bill_id = bill_id
        self.customer_phone_no = customer_phone_no
        self.customer_name = customer_name
        self.items = items
        self.quantity = quantity
        self.table_number = table_number
        self.price = price
        self.total_amount = total_amount
        self.date_time = date_time

    def __str__(self):
        return {
            "bill id" : {self.bill_id},
            "customer_phone_no" : {self.customer_phone_no},
            "custmer name "  : {self.customer_name},
            "items"  : {self.items},
            "quantity" : {self.quantity},
           " table_number" : {self.table_number},
            "price" : {self.price},
            "total amount" : {self.total_amount},
            "date_time" : {self.date_time}
        }
    
        
        

