import re

def validate_id(id):
    if(len(id)==6):
        return id.upper()
    else:
        return False
    
def customer_name_validate(name):

    pattern  = r"^[A-Za-z]+$"
    if(re.match(pattern, name)):
        return name.upper()
    else:
        return False

def table_number_validate(table_number):
    pattern = r"^[0-9]$"
    if(re.match(pattern, table_number)):
        return table_number.upper()
    else:
        return False
    

def quantity_validate(quantity):
    pattern =r"^(?:[1-9]|[1-4][0-9]|50)$"
    if(re.match(pattern, quantity)):
        return quantity
    else:
        return False


def validate_item(items):
    pattern =r'^[A-Za-z]+$'
    if(re.match(pattern, items)):
        return items.upper()
    else:
        return False
    
def valide_phone_no(phone_no):
    pattern = r"^[1-9]\d{9}$"
    if(re.match(pattern, phone_no)):
        return phone_no
    else:
        return False
    
   
    
    


    

    

    

    


