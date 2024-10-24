import re

def validate_id(id):
    if(len(id)==6):
        return id.upper()
    else:
        return False
    
def customer_name_validate(name):

    pattern  = r"^[A-Za-z]$"
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
    
    
    
    
    


    

    

    

    


