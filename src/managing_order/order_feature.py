from src.managing_order.manage_order import ManageOrder
from src.utility.validation import*
from src.utility.check_order import check_order

class OrderFeature(ManageOrder):
    def order(self):
        try:
            while True:
                name = customer_name_validate(input("Enter the customer name : "))
                if(not name):
                    raise Exception("Enter a valid customer name ")

                modile_no = valide_phone_no(input("Enter modile number : "))
                if(not modile_no):
                    raise Exception("Enter a valid mobile no")
                
                table_number = input("Enter table")
                if
                


                item = validate_item(input("Enter the item name : "))
                if(not item):
                    raise Exception("Enter a valid item")
                
                quantity = quantity_validate(input("Enter the quantity of the item : "))
                if(not quantity):
                    raise Exception("Enter a valid quantity")
                
                price = input("Enter the price of the item : ")
                if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
                    raise Exception("Enter a valid price")
                
                add_more = input("Do you want to add another item? (yes/no): ").strip().upper()
                if add_more != 'yes':
                    break
                print("Bill created successfully")

        except Exception as error:
            print(error)

        

            
    def update_item(self):
        try:
            while True:
                item = validate_item(input("Enter the item name : "))
                if(not item):
                    raise Exception("Enter a valid item")
                
                quantity = quantity_validate(input("Enter a valid quantity"))
                if(not quantity):
                    raise Exception("Enter the quantity of the item : ")
                
                price = input("Enter the price of the item : ")
                if not price.replace('.', '', 1).isdigit() or int(price) <= 0:
                    raise Exception("Enter a valid price")
                
                add_more = input("Do you want to add another item? (yes/no): ").strip().upper()
                if add_more != 'yes':
                    break
                print("Bill updated  successfully")

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

            


            




            


            
        







            
            
    

