from src.Manage_bill.manage_bill import ManageBill
from src.utility.validation import*
from src.Manage_bill.manage_bill import ManageBill


class BillFeature(ManageBill):
    def bill(self):
        try:
            while True:
                item = input("Enter the item name : ")
                if(not item):
                    raise Exception("Enter a valid item")
                
                quantity = input("Enter the quantity of the item: ")
                if not quantity.isdigit() or int(quantity) <= 0:
                    raise Exception("Enter a valid quantity")
                
                price = input("Enter the price of the item: ")
                if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
                    raise Exception("Enter a valid price")
                
        except Exception as error:
            print(error)

    def search_bill(self, bill_id):
        try:
            id = validate_id(input("Enter a valid id : "))
            if(not bill_id):
                raise Exception("please enter a valid id ")
            self.get_bill(bill_id)
        
        except Exception as error:
            print(error)
            

    def search_all_bill(self):
        try:
            self.get_all_bill()
        
        except Exception as error:
            print(error)




                    
                
                
                
        
        