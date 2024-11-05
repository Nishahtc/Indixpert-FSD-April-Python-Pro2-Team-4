import uuid
from datetime import datetime
from src.Manage_bill.bill_model import BillModel
from src.Manage_bill.bill import Bill
from src.use


class ManageBill(Bill):

    def create_bill(self, bill_id, customer_name, customer_phone_no, items, quantity, table_number, price,total_amount,  date_time ):
        bill_id = str(uuid.uuid4())[:6]
        date_time = datetime.now()
        total_amount = sum(qty * price for qty, price in zip(quantity, price))
        new_bill = BillModel(self, bill_id, customer_name, customer_phone_no, items, quantity, table_number, price, total_amount, date_time)
        self.bills.append(new_bill)
        self.save_bill()
        print(f"{'ID':<10}   {'customer phone_no': <15}  {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'price ' :<20} {'Total Amount':<15} {'Order Date':<20}")
        print('-' * 155)


    def update_bill(self, bill_id, items, quantity, price, total_amount):
        for bill in self.bills:
            if(bill.bill_id == bill_id):
                bill.items = items
                bill.quantity = quantity
                bill.price = price
                total_amount = sum(qty * price for qty, price in zip(quantity, price))
                self.save_bill()
                print(f"Bill updated successfully. Total amount: {total_amount}")
                break

        else:
            print(f'bill not found for ID : {id}')


    def delete(self, bill_id):
        for bill in self.bills:
            if(bill.bill_id == bill_id):
                self.bills.remove(bill)
                self.save_bill()
                print("Bill deleted successfully")
      

    def get_bill(self, bill_id):
        for bill in self.bills:
            if(bill.bill_id == bill_id ):
                print(f"{'ID':<10} {'customer phone_no' :<15} {'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'price':<20} {'Total Amount':<15} {'Order Date':<20}")
                print(f'  -'*155)
                print(f"{bill.bill_id:<10}  {bill.customer_phone_no :<15} {bill.customer_name:<20} {bill.table_number:<15} {bill.items:<30} {bill.quantity:<10}  {bill.price:<20}{bill.total_amount:<15} {bill.date_time.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                break
        
        else:
            print("bill not found")


    def get_all_bill(self):
        print(f"{'ID':<10}   {'customer phone_no': <15}{'Customer Name':<20} {'Table Number':<15} {'Items':<30} {'Quantity':<10} {'Total Amount':<15} {'Order Date':<20}")
        print('-' * 135)
        if(len(self.bills))>0:
            for bill in self.bills:
                print(f"{bill.bill_id:<10} {bill.customer_phone_no} {bill.customer_name:<20} {bill.table_number:<15} {bill.items:<30} {bill.quantity:<10} {bill.total_amount:<15} {bill.date_time.strftime('%Y-%m-%d %H:%M:%S'):<20}")
                print('*'*135)
                
        else:
            print("bill no found")
                   
