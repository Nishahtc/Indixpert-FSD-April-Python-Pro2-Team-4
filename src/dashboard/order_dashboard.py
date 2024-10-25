from src.managing_order.order_feature import OrderFeature

def order_menu():
    order = OrderFeature()
    
    while True:
        print(f'\n***********************Welcome*********************')
        print(f'-----------------------------------------------------------------------')
        print(f'1 ADD ORDER')
        print(f'2 UPDATE ORDER')
        print(f'3 DELETE ORDER')
        print(f'4 SEARCH ORDER')
        print(f'5 VIEW ALL ORDER')
        print(f'********************************************************************\n')

        choice = int(input('Please Chooose Any Option : '))
        if(choice == 1):
            order.order()
            
        elif(choice == 2):
            order.update_item()

        elif(choice == 3):
            order.cancel_item()

        elif(choice == 4):
            order.search_order()

        elif(choice == 5):
            order.search_all_order()

        else:
            print("Please choose a valid option")
            
  
            