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
            order.()
            
  
            