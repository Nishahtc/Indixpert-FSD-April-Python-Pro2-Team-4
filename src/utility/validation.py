import re

def validate_id(id):
    if(len(id)==4):
        return id.upper()
    
def validate_items(items):
    pattern = r'^\s*[^,\s]+(\s*,\s*[^,\s]+:\s*[1-9]\d*)*\s*$'
    if(re.match(pattern,items)):
       return items.upper()
    else:
        return False
    

