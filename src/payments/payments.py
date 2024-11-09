import json
import os
from datetime import datetime
from src.utility.validations import validate_phone_number

DATABASE_FOLDER = "src/database"
PAYMENT_FILE_PATH = os.path.join(DATABASE_FOLDER, "payment.json")

class Payment:
    def __init__(self, amount, method, customer_name, mobile_number, order_id=None):
        self.customer_name = customer_name
        self.amount = amount
        self.method = method
        self.mobile_number = validate_phone_number(mobile_number)
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
            print("Corrupted payment file. Initializing new payment file.")
            payments = []

    payments.append(payment.to_dict())
    with open(filename, 'w') as file:
        json.dump(payments, file, indent=4)

def search_payments(query, search_type="mobile"):
    if not os.path.exists(PAYMENT_FILE_PATH):
        print("No payment records found.")
        return []

    with open(PAYMENT_FILE_PATH, 'r') as file:
        payments = json.load(file)

    if search_type == "mobile":
        return [p for p in payments if p['mobile_number'] == query]
    elif search_type == "order_id":
        return [p for p in payments if p['order_id'] == query]

def process_payment():
    try:
        amount = float(input("Enter payment amount: "))
        method = input("Enter payment method (e.g., cash, online, credit card): ").strip()
        customer_name = input("Enter customer name: ").strip()
        # mobile_number = input("Enter mobile number: ").strip()
        payment = Payment(amount, method, customer_name)
        save_payment(payment)
        print("Payment processed successfully!")
    except ValueError as e:
        print(f"Error: {e}")
