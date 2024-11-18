import re
import json
import os

BOOKING_FILE_PATH = "src/database/booking.json"

def has_reached_booking_limit(customer_name):
    if not os.path.exists(BOOKING_FILE_PATH):
        return False

    try:
        with open(BOOKING_FILE_PATH, 'r') as file:
            tables = json.load(file)
            total_bookings = 0
            for table_info in tables.values():
                for date, slots in table_info.items():
                    for slot, booking in slots.items():
                        if booking and booking['customer'].lower() == customer_name.lower():
                            total_bookings += 1
                            if total_bookings >= 5:
                                return True
        return False
    except json.JSONDecodeError:
        print("Error loading booking data.")
        return False
    
def validate_id(id_value):
    if len(id_value) == 6 and id_value.isalnum():
        return id_value.upper()
    return False

def customer_name_validate(name):
    pattern = r"^[A-Za-z\s]+$"
    if re.match(pattern, name):
        return name.lower()
    return False

# def validate_meal_type(meal_type):
#     pattern = r"^[A-Za-z\s]+$"
#     if re.match(pattern, meal_type):
#         return meal_type.strip().lower().replace(" ", "_")
#     return False

def table_number_validate(table_number):
    if isinstance(table_number, str) and table_number.isdigit():
        table_number = int(table_number)
        if 1 <= table_number <= 99:
            return table_number
    return False

def validate_phone_number(phone_number):
    pattern = r"^[0-9]{10}$"
    if re.match(pattern, phone_number):
        return phone_number
    return False

def validate_item(item_name):
    pattern = r"^[A-Za-z0-9\s\-]+$"
    if re.match(pattern, item_name):
        return item_name.title()
    return False

# def validate_quantity(quantity):
#     if quantity.isdigit() and int(quantity) > 0:
#         return int(quantity)
#     return False

# def validate_price(price):
#     try:
#         price = int(price)
#         if price > 0:
#             return price
#     except ValueError:
#         return False
#     return False

# def validate_meal_type(meal_type):
#     valid_meals = [
#         "breakfast", "lunch", "dinner", "snacks", 
#         "soups", "starters", "main_course", "noodles",
#         "rice", "desserts", "tea_and_coffee", "ice_cream"
#     ]
#     if meal_type in valid_meals:
#         return meal_type
#     return None

def admin_check(users):
    for user in users:
        if user.get('role') == 'admin':
            return True
    return False

def is_username_taken(users, username):
    for user in users:
        if user.get('username') == username:
            return True
    return False

def validate_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_mobile_number(mobile_number):
    return mobile_number.isdigit() and len(mobile_number) == 10

