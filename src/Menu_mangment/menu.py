import json
import os

DATABASE_FOLDER = "src/database"
MENU_FILE_PATH = os.path.join(DATABASE_FOLDER, "menu.json")

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price}"

    @classmethod
    def from_dict(cls, item_dict):
        return cls(item_dict['name'], item_dict['price'])

class Menu:
    MEAL_TYPES = [
        "breakfast", "lunch", "dinner", "snacks",
        "soups", "starters", "main_course", "noodles",
        "rice", "desserts", "tea_and_coffee",
        "ice_cream \n"
    ]

    def __init__(self, menu_file=MENU_FILE_PATH):
        if not os.path.exists(DATABASE_FOLDER):
            os.makedirs(DATABASE_FOLDER)

        self.file = menu_file
        self.menu_data = self.load_menu()

    def load_menu(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                try:
                    menu_data = json.load(f)
                    return {meal: [MenuItem.from_dict(item) for item in items] for meal, items in menu_data.items()}
                except json.JSONDecodeError:
                    print("Error loading menu. Starting with an empty menu.")
        
        return {meal: [] for meal in self.MEAL_TYPES}

    def save_menu(self):
        with open(self.file, 'w') as file:
            json.dump({meal: [item.__dict__ for item in items] 
            for meal, items in self.menu_data.items()}, file, indent=4)

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
                print(f"  {index}. {item}")

    def add_item(self, meal_type, name, price):
        new_item = MenuItem(name, price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        print(f"Added to {meal_type}: {new_item}")
        print("\n-------- Add Successfully ---------")

    def delete_item(self, meal_type, index):
        if meal_type not in self.menu_data:
            print(self.ERROR_INVALID_MEAL_TYPE)
            return
        if index < 0 or index >= len(self.menu_data[meal_type]):
            print(self.ERROR_INVALID_INDEX)
            return

        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        print(f"Deleted from {meal_type}: {removed_item}")
        print("\n-------- Delete Successfully --------")

    def update_item(self, meal_type, index, name=None, price=None):
        if meal_type not in self.menu_data or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index.")
            return
        item = self.menu_data[meal_type][index]
        if name:
            item.name = name
        if price is not None:
            item.price = price
        self.save_menu()
        print(f"Updated in {meal_type}: {item}")
        print("\n-------- Update Successfully --------")

def main():
    menu = Menu()
    
    while True:
        print("\nMenu Management System")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Delete Menu Item")
        print("4. Update Menu Item")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            print("------------------------------")
            print("    ******MENU LIST******     ")
            print("------------------------------")
            print("\nAvailable meal types:")
            for i, meal in enumerate(Menu.MEAL_TYPES, start=1):
                print(f"  {i}. {meal.capitalize()}")
               
            meal_type = input("Enter meal type: ").strip().lower()
            menu.view_menu(meal_type)
            
        elif choice == '2':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
                print("Invalid meal type.")
                continue
            name = input("Enter item name: ")
            price_input = input("Enter item price: ")
            
            try:
                if not price_input:
                    raise ValueError("Price cannot be empty.")
                price = float(price_input)
                if price < 0:
                    raise ValueError("Price cannot be negative.")
                menu.add_item(meal_type, name, price)
            except ValueError as ve:
                print(f"Invalid price: {ve}")
                
        elif choice == '3':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
              
                continue
            menu.view_menu(meal_type)  
            index_input = input("Enter item index to delete: ")

            try:
                index = int(index_input) 
                menu.delete_item(meal_type, index)
            except ValueError:
                print("Invalid input. Please enter a valid numeric index.")

        
        elif choice == '4':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
                print("Invalid meal type.")
                continue
            menu.view_menu(meal_type)
            index = input("Enter item index to update: ")

            try:
                index = int(index)
                name = input("Enter new item name (leave blank for no change): ").strip()
                price_input = input("Enter new item price (leave blank for no change): ").strip()
                new_name = name if name else None
                new_price = float(price_input) if price_input else None

                menu.update_item(meal_type, index, new_name, new_price)
            except ValueError:
                print("Invalid input. Please enter a valid numeric index or a valid price.")

        elif choice == '5':
            print("Exiting the menu management system.")
            break

main()
