import json
import os
from datetime import datetime

DATABASE_FOLDER = "src/database"
PAYMENT_FILE_PATH = os.path.join(DATABASE_FOLDER, "payment.json")

class Payment:
    def __init__(self, amount, method, customer_name, mobile_number, order_id=None):
        self.customer_name = customer_name
        self.amount = amount
        self.method = method
        self.mobile_number = mobile_number
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
        """Generate an automatic order ID based on the number of existing entries in payment.json."""
        order_number = self.get_next_order_number()
        return f"SO-{order_number:03d}"

    def get_next_order_number(self):
        """Get the next order number based on the current number of records in payment.json."""
        if os.path.exists(PAYMENT_FILE_PATH):
            try:
                with open(PAYMENT_FILE_PATH, 'r') as file:
                    payments = json.load(file)
                    next_order_number = len(payments) + 1  
            except (json.JSONDecodeError, IOError):
                next_order_number = 1  
        else:
            next_order_number = 1  
        return next_order_number

def validate_payment(payment):
    if payment.amount <= 0:
        raise ValueError("Payment amount must be positive.")
    if not payment.method:
        raise ValueError("Payment method cannot be empty.")
    if not payment.customer_name:
        raise ValueError("Customer name cannot be empty.")
    if not payment.mobile_number:
        raise ValueError("Mobile number cannot be empty.")
    return True

def save_payment(payment, filename=PAYMENT_FILE_PATH):
    os.makedirs(DATABASE_FOLDER, exist_ok=True) 

    try:
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    payments = json.load(file)
            except (json.JSONDecodeError, IOError):
                payments = []  
        else:
            payments = [] 

        payments.append(payment.to_dict())

        with open(filename, 'w') as file:
            json.dump(payments, file, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving payment data: {e}")

def search_payments(query, search_type="mobile"):
    """Search payments by mobile number or order ID."""
    if not os.path.exists(PAYMENT_FILE_PATH):
        print("No payment records found.")
        return []

    try:
        with open(PAYMENT_FILE_PATH, 'r') as file:
            payments = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading payment records: {e}")
        return []

    results = []
    if search_type == "mobile":
        results = [p for p in payments if p['mobile_number'] == query]
    elif search_type == "order_id":
        results = [p for p in payments if p['order_id'] == query]
    return results

def process_payment():
    try:
        amount = input("Enter payment amount: ")
        amount = float(amount) if amount.replace('.', '', 1).isdigit() else None
        if amount is None or amount <= 0:
            raise ValueError("Invalid amount. Please enter a valid number greater than 0.")
        
        method = input("Enter payment method (e.g., cash, online, credit card): ").strip()
        customer_name = input("Enter customer name: ").strip()
        mobile_number = input("Enter mobile number: ").strip()

        payment = Payment(amount, method, customer_name, mobile_number)
        
        if validate_payment(payment):
            save_payment(payment)
            print("Payment processed successfully!")
            print(f"Payment Date & Time: {payment.added_on}")
            print(f"Order ID: {payment.order_id}")
    except ValueError as e:
        print(f"Error: {e}")

def display_search_results(results):
    if results:
        for payment in results:
            print("\nPayment Details:")
            print(f"Customer Name: {payment['customer_name']}")
            print(f"Amount: {payment['amount']}")
            print(f"Method: {payment['method']}")
            print(f"Mobile Number: {payment['mobile_number']}")
            print(f"Order ID: {payment['order_id']}")
            print(f"Date & Time: {payment['added_on']}")
    else:
        print("No results found.")

def main():
    while True:
        print("\n1. Process a payment")
        print("2. Search payments by Mobile Number")
        print("3. Search payments by Order ID")
        print("4. Exit")
        
        choice = input("Choose an option: ").strip()

        if choice == '1':
            process_payment()
        elif choice == '2':
            mobile_number = input("Enter mobile number to search: ").strip()
            results = search_payments(mobile_number, search_type="mobile")
            display_search_results(results)
        elif choice == '3':
            order_id = input("Enter Order ID to search: ").strip()
            results = search_payments(order_id, search_type="order_id")
            display_search_results(results)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
