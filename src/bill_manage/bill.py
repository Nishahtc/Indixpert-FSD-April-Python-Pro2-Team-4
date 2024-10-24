import json
import os
from src.bill_manage.bill_model import BillModel
BILL_FILE = "src/database/bill.json"

class Bill:
    def __init__(self):
        self.bills = self.load_bill()

    def load_bill(self):
        if os.path.exists(BILL_FILE):
            with open(BILL_FILE,'r') as file:
                all_bill =json.load(file)
                return [BillModel(**bill) for bill in all_bill]
            
        else:
            return []
        
    def save_load(self):
        with open(BILL_FILE, 'w') as file:
            all_bill = [bill.__dic__ for bill in self.bills]
            json.dump(all_bill, file, indent=4)
        

            
            
            
            
            