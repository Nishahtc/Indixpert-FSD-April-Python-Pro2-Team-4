import re

def validate_id(id_value):
    if len(id_value) == 6 and id_value.isalnum():
        return id_value.upper()
    return False

def customer_name_validate(name):
    pattern = r"^[A-Za-z\s]+$"
    if re.match(pattern, name):
        return name.lower()
    return False

def validate_meal_type(meal_type):
    pattern = r"^[A-Za-z\s]+$"
    if re.match(pattern, meal_type):
        return meal_type.strip().lower().replace(" ", "_")
    return False

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

def validate_quantity(quantity):
    if quantity.isdigit() and int(quantity) > 0:
        return int(quantity)
    return False

def validate_price(price):
    try:
        price = int(price)
        if price > 0:
            return price
    except ValueError:
        return False
    return False

def validate_meal_type(meal_type):
    valid_meals = [
        "breakfast", "lunch", "dinner", "snacks", 
        "soups", "starters", "main_course", "noodles",
        "rice", "desserts", "tea_and_coffee", "ice_cream"
    ]
    if meal_type in valid_meals:
        return meal_type
    return None

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

