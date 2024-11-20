import uuid
from src.manage_bill.bill_model import BillModel
from src.manage_bill.bill import Bill
from src.utility.messages import messages

class ManageBill(Bill):
    def create_bill(
        self,
        customer_name,
        customer_phone_no,
        table_number,
        items,
        quantities,
        item_totals,
        total_amount,
        order_type=None,
        payment_info=None,
    ):

        bill_id = str(uuid.uuid4())[:6]
        new_bill = BillModel(
            bill_id=bill_id,
            customer_name=customer_name,
            customer_phone_no=customer_phone_no,
            table_number=table_number,
            items=items,
            quantities=quantities,
            item_totals=item_totals,
            total_amount=total_amount,
            order_type=order_type,
            payment_info=payment_info,
        )
        self.bills.append(new_bill)
        self.save_bills()
        print(f"Bill created successfully with ID: {bill_id}")
        return new_bill

    def update_bill(self, bill_id, updated_data):
        for bill in self.bills:
            if bill.bill_id == bill_id:
                for key, value in updated_data.items():
                    setattr(bill, key, value)
                self.save_bills()
                print(f"Bill with ID {bill_id} updated successfully.")
                return bill
        raise ValueError(f"Bill with ID {bill_id} not found.")

    def delete_bill(self, bill_id):
        initial_count = len(self.bills)
        self.bills = [bill for bill in self.bills if bill.bill_id != bill_id]
        if len(self.bills) < initial_count:
            self.save_bills()
            print(f"Bill with ID {bill_id} deleted successfully.")
        else:
            print(f"Bill with ID {bill_id} not found.")

    def get_bill(self, bill_id):
        for bill in self.bills:
            if bill.bill_id == bill_id:
                return bill
        print(f"No bill found with ID: {bill_id}")
        return None

    def get_all_bills(self):
        if self.bills:
            print("\nAll Bills:")
            for bill in self.bills:
                print(bill)
            return self.bills
        else:
            print(messages.no_bills_found)
            return []
