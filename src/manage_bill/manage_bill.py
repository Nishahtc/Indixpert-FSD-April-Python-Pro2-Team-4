import uuid
from src.manage_bill.bill_model import BillModel
from src.manage_bill.bill import Bill
from src.utility.messages import messages

class ManageBill(Bill):
    def create_bill(self, customer_name, customer_phone_no, table_number, items, quantities, item_totals, total_amount, order_type=None, payment_info=None):
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
            payment_info=payment_info
        )
        self.bills.append(new_bill)
        self.save_bills()
        print("Bill created successfully with payment details.")

    # def update_bill(self, bill_id, items, quantities, prices):
    #     for bill in self.bills:
    #         if bill.bill_id == bill_id:
    #             bill.items = items
    #             bill.quantities = quantities
    #             bill.prices = prices
    #             bill.total_amount = sum(qty * price for qty, price in zip(quantities, prices))
    #             self.save_bills()
    #             print("Bill updated successfully.")
    #             return
    #     print(f"Bill not found with the given ID: {bill_id}")

    # def delete(self, bill_id):
    #     for bill in self.bills:
    #         if bill.bill_id == bill_id:
    #             self.bills.remove(bill)
    #             self.save_bills()
    #             print("Bill deleted successfully.")
    #             return
    #     print(f"Bill not found with the given ID: {bill_id}")

    # def get_bill(self, bill_id):
        # for bill in self.bills:
        #     if bill.bill_id == bill_id:
        #         print(bill)
        #         return
        # print(f"Bill not found with the given ID: {bill_id}")

    def get_all_bills(self):
        if self.bills:
            print("\n" + "=" * 30 + "\n      All Restaurant Bills\n" + "=" * 30)
            for bill in self.bills:
                print(bill)
                print("\n" + "=" * 30)
        else:
            print(messages.no_bills_found)
