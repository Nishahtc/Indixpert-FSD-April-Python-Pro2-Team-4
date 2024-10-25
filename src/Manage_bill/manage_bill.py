import uuid
from datetime import datetime
from src.bill_manage.bill_model import BillModel
from src.bill_manage.bill import Bill
from src.use


class ManageBill(Bill):
    def create_bill(self, bill_id, customer_name, customer_phone_no, items, quantity, total_amount, date_time ):
        id = str(uuid.uuid4())[:6]
        date_time = date_time.now()
        

    def get_bill(self, bill_id):
        for bill in self.bills:
            if(bill.bill_id == bill_id ):
                print(f"{'ID':<10} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
                print(f' \n -'*120)
                print(f"{bill.bill_id:<10} {bill.customer_name:<20} {bill.table_number:<15} {bill.items:<30} {bill.quantity:<10} {bill.total_amount:<15} {bill.date_time.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                break
        
        else:
            print("bill not found")
    

    def get_all_bill(self):
        print(f"{'ID':<10} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
        print('-' * 120)
        if(len(self.bills))>0:
            for bill in self.bills:
                print(f"{bill.bill_id:<10} {bill.customer_name:<20} {bill.table_number:<15} {bill.items:<30} {bill.quantity:<10} {bill.total_amount:<15} {bill.date_time.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                print('*'*120)
                
        else:
            print("bill no found")
                






        

   

