class MenuItem:
    def __init__(self, name,  price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}:{self.price}"


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        new_item = MenuItem(name,  price)
        self.items.append(new_item)
        print(f"Added: {new_item}")

    def view_menu(self):
        if not self.items:
            print("Menu is empty.")
            return
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item}")


    def delete_item(self, index):
        if index < 0 or index >= len(self.items):
            print("Invalid index.")
            return
        removed_item = self.items.pop(index)
        print(f"Deleted: {removed_item}")


def main():
    menu = Menu()
    
    while True:
        print("\n1. Add Menu Item\n2. View Menu\n3. Delete Menu Item\n")
        choice = input("Choose an option: ")
        
        if choice == '1':
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            menu.add_item(name, price)
        
        elif choice == '2':
            menu.view_menu()

        elif choice == '3':
            index = int(input("Enter item index to delete: ")) 
            menu.delete_item(index)

        else:
            print("Invalid choice. Please try again.")


main()
