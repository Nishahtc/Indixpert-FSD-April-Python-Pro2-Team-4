from src.managing_order.manage_order import ManageOrder
from src.utility.validation import*
from src.utility.check_order import check_order

class OrderFeature(ManageOrder):
    def order(self):
        try:
            customer_name = customer_name_validate(input("Enter customer name : "))
            if(not customer_name):
                raise Exception("You can't enter empty name")
            
            table_number = input("Enter table number") # i should call table method or make valid
            if(not table_number):
                raise Exception("please enter valid table number")
            
            items = input(f"what you want to try today \n please order : ")# same
            if(not items):
                raise Exception("please enter a valid item")
            
            quantity = input("please enter quantity : ")
            if(not quantity):
                raise Exception("please enter valid quantity")
            
            #  add amount here 
            self.add_order(customer_name, table_number, items, quantity)

        except Exception as error:
            print(error)

            
    def update_item(self):
        try:
            customer_name = customer_name_validate(input("Enter customer name : "))
            if(not customer_name):
                raise Exception("enter valid name ")
            
            items = input("Enter your order item which u want to update : ")
            if(not items):
                raise Exception("enter valid item")
            
            table_number = input("Enter table number : ")
            if(not table_number):
                raise Exception("enter valid table number")
            
            quantity = input("Enter quantity : ")
            if(not quantity):
                raise Exception("enter valid quantity")
            
            self.update_order(customer_name, items,table_number, quantity)

        except Exception as error:
            print(error)

    def cancel_item(self):
        try:
            id = validate_id(input("Enter id : "))
            if(not id):
                raise Exception("enter valid id")
            
            self.cancel_order(id)

        except Exception as error:
            print(error)

    
    def search_order(self):
        try:
            id = validate_id(input("Enter id : "))
            if(not id):
                raise Exception("enter valid id")
            
            self.get_order(id)

        except Exception as error:
            print(error)


    def search_all_order(self):
        try:
            self.get_all_order() 

        except Exception as error:
            print(error)  

            


            




            


            
        







            
            
    

