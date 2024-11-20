import json
import os
from src.manage_bill.bill_model import BillModel

BILL_FILE = "src/database/bill.json"

class Bill:
    def __init__(self):
        self.bills = self.load_bills()

    def load_bills(self):
        if os.path.exists(BILL_FILE):
            with open(BILL_FILE, 'r') as file:
                all_bills = json.load(file)
                return [BillModel(**bill) for bill in all_bills]
        return []

    def save_bills(self):
        with open(BILL_FILE, 'w') as file:
            all_bills = [bill.__dict__ for bill in self.bills]
            json.dump(all_bills, file, indent=4)
