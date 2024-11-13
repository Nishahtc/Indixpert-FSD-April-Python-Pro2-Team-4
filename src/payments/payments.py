import json
import os
from datetime import datetime
from src.utility.validations import validate_phone_number
from src.utility.messages import Messages

DATABASE_FOLDER = "src/database"
PAYMENT_FILE_PATH = os.path.join(DATABASE_FOLDER, "payment.json")

class Payment:
    def __init__(self, amount, method, customer_name, mobile_number=None, order_id=None):
        self.customer_name = customer_name
        self.amount = amount
        self.method = method
        self.mobile_number = validate_phone_number(mobile_number) if mobile_number else None
        self.order_id = order_id if order_id else self.generate_order_id()
        self.added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'customer_name': self.customer_name,
            'amount': self.amount,
            'method': self.method,
            'mobile_number': self.mobile_number,
            'order_id': self.order_id,
            'added_on': self.added_on
        }

    def generate_order_id(self):
        order_number = self.get_next_order_number()
        return f"SO-{order_number:03d}"

    def get_next_order_number(self):
        if os.path.exists(PAYMENT_FILE_PATH):
            with open(PAYMENT_FILE_PATH, 'r') as file:
                payments = json.load(file)
                return len(payments) + 1
        return 1

def save_payment(payment, filename=PAYMENT_FILE_PATH):
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    payments = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                payments = json.load(file)
        except json.JSONDecodeError:
            Messages.corrupted_payment_file()
            payments = []

    payments.append(payment.to_dict())
    with open(filename, 'w') as file:
        json.dump(payments, file, indent=4)
    Messages.payment_saved_successfully()

def search_payments(query, search_type="mobile"):
    if not os.path.exists(PAYMENT_FILE_PATH):
        Messages.no_payment_records()
        return []

    with open(PAYMENT_FILE_PATH, 'r') as file:
        payments = json.load(file)

    if search_type == "mobile":
        return [p for p in payments if p['mobile_number'] == query]
    elif search_type == "order_id":
        return [p for p in payments if p['order_id'] == query]

def process_payment():
    try:
        amount = float(input(Messages.enter_payment_amount()))
        method = input(Messages.enter_payment_method()).strip()
        customer_name = input(Messages.enter_customer_name()).strip()
        mobile_number = input(Messages.enter_mobile_number()).strip()
        payment = Payment(amount, method, customer_name, mobile_number)
        save_payment(payment)
        Messages.payment_processed_successfully()
    except ValueError as e:
        Messages.error_message(e)
