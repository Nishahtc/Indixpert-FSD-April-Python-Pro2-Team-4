import re

def validate_id(id):
    if(len(id)==4):
        return id.upper()
    else:
        return False
    
def customer_name_validate(name):

    pattern  = r"^[A-Za-z]$"

    if(re.match(pattern, name)):
        return name.upper()
    else:
        return False
    

    

    

    

    


