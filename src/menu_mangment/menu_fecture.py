import json
import os

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price}"

class Menu:
    def __init__(self, filename='menu.json'):
        self.filename = filename
        self.menu_data = self.load_menu()

    def load_menu(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {meal: [] for meal in []}

    def save_menu(self):
        with open(self.filename, 'w') as file:
            json.dump(self.menu_data, file, indent=4)

    def view_menu(self, meal_type):
        if meal_type not in self.menu_data:
            print("Invalid meal type.")
            return
        items = self.menu_data[meal_type]
        print(f"\n{meal_type.capitalize()}:")
        if not items:
            print("  No items.")
        else:
            for index, item in enumerate(items, start=1):
                print(f"  {index}. {MenuItem(item['name'], item['price'])}")

    def add_item(self, meal_type, name, price):
        new_item = {"name": name, "price": price}
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        print(f"Added to {meal_type}: {new_item}")

    def delete_item(self, meal_type, index):
        if meal_type not in self.menu_data or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index.")
            return
        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        print(f"Deleted from {meal_type}: {removed_item}")

    def update_item(self, meal_type, index, name=None, price=None):
        if meal_type not in self.menu_data or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index.")
            return
        item = self.menu_data[meal_type][index]
        if name:
            item['name'] = name
        if price is not None:
            item['price'] = price
        self.save_menu()
        print(f"Updated in {meal_type}: {item}")

def main():
    menu = Menu()
    
    while True:
        print("\nMenu Management System")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Delete Menu Item")
        print("4. Update Menu Item")
        
        choice = input("Choose an option: ")

        if choice == '1':
            print("------------------------------")
            print("    ******MENU LIST******     ")
            print("------------------------------")
            print("\n1.breakfast","\n2.lunch","\n3.dinner","\n4.snacks", "\n5.soups","\n6.starters","\n7.main_course","\n8.noodles",
                  "\n9.rice","\n10.desserts","\n11.extras","\n12.tea_and_coffee","\n13.aerated_beverages","\n14.ice_cream" )
            print()
            meal_type = input("Enter meal type: ").strip().lower()
            menu.view_menu(meal_type)
            
        elif choice == '2':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in menu.menu_data:
                print("Invalid meal type.")
                continue
            name = input("Enter item name: ")
            price_input = input("Enter item price: ")
            try:
                price = float(price_input)
                if price < 0:
                    raise ValueError("Price cannot be negative.")
                menu.add_item(meal_type, name, price)
            except ValueError as ve:
                print(f"Invalid price: {ve}")
                
        elif choice == '3':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in menu.menu_data:
                print("Invalid meal type.")
                continue
            menu.view_menu(meal_type)  
            index = input("Enter item index to delete: ")
            try:
                index = int(index) - 1
                menu.delete_item(meal_type, index)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid numeric index.")
                
        elif choice == '4':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in menu.menu_data:
                print("Invalid meal type.")
                continue
            menu.view_menu(meal_type) 
            index = input("Enter item index to update: ")
            try:
                index = int(index) - 1
                name = input("Enter new item name: ")
                price_input = input("Enter new item price: ")
                price = float(price_input) if price_input else None
                if price is not None and price < 0:
                    raise ValueError("Price cannot be negative.")
                menu.update_item(meal_type, index, name if name else None, price)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid numeric index or a valid price.")

main()
