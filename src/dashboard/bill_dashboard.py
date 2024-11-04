from src.Manage_bill.bill_feature import BillFeature

def bill_menu():
    bill = BillFeature()

    while True:
        print(f'\n***********************One Bite*********************')
        print(f'-----------------------------------------------------------------------')
        print(f'1 CREATE BILL')
        print(f'2 UPDATE BILL')
        print(f'3 DELETE BILL')
        print(f'4 SEARCH BILL')
        print(f'5 VIEW ALL BILL')
        print(f'********************************************************************\n')

        choice = int(input('Please Chooose Any Option : '))
        if(choice == 1):
            bill.bill_create()

        elif(choice == 2):
            bill.update()

        elif(choice == 3):
            bill.delete_bill()

        elif(choice == 4):
            bill.search_bill()

        elif(choice == 5):
            bill.search_all_bill()

        else:
            print("Please choose a valid option")
                
       