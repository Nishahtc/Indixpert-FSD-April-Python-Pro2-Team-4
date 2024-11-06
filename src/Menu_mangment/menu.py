import json
import os

DATABASE_FOLDER = "src/database"
MENU_FILE_PATH = os.path.join(DATABASE_FOLDER, "menu.json")

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price:.2f}"

    @classmethod
    def from_dict(cls, item_dict):
        return cls(item_dict['name'], item_dict['price'])

class Menu:
    MEAL_TYPES = [
        "breakfast", "lunch", "dinner", "snacks", 
        "soups", "starters", "main_course", "noodles",
        "rice", "desserts", "tea_and_coffee", "ice_cream"
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
            json.dump({meal: [item.__dict__ for item in items] for meal, items in self.menu_data.items()}, file, indent=4)

    def view_menu(self):
        print("\n" + "*" * 30 + " MENU " + "*" * 30)

        for meal_type, items in self.menu_data.items():
            print(f"\n{'*' * (20 - len(meal_type) // 2)}{meal_type.upper()}{'*' * (20 - len(meal_type) // 2)}")

            if not items:
                print("  No items available.")
            else:
                print(f"\n{'S No.':<10}{'NAME':<30}{'RATE':<10}")
                print("-" * 50)  
                for index, item in enumerate(items):
                    print(f"{index + 1:<10}{item.name:<30}{item.price:<10.2f}")
    
        print("\n" + "*" * 60)

    def add_item(self, meal_type, name, price):
        if meal_type not in self.MEAL_TYPES:
            print(f"Invalid meal type: {meal_type}.")
            return
        if not name:
            print("Item name cannot be empty.")
            return
        if price <= 0:
            print("Price must be a positive number.")
            return

        new_item = MenuItem(name, price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        print(f"Added to {meal_type}: {new_item}")

    def remove_item(self, meal_type, index):
        if meal_type not in self.MEAL_TYPES or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index or meal type.")
            return
        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        print(f"Removed from {meal_type}: {removed_item}")

    def update_item(self, meal_type, index, name=None, price=None):
        if meal_type not in self.MEAL_TYPES or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index or meal type.")
            return
        item = self.menu_data[meal_type][index]
        if name:
            item.name = name
        if price is not None:
            if price <= 0:
                print("Price must be a positive number.")
                return
            item.price = price
        self.save_menu()
        print(f"Updated item in {meal_type}: {item}")

def main():
    menu = Menu()
    
    while True:
        print("\nMenu Management System")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Remove Menu Item")
        print("4. Update Menu Item")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            menu.view_menu()
        elif choice == '2':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
                print("Invalid meal type.")
                continue
            name = input("Enter item name: ").strip()
            price_input = input("Enter item price: ").strip()

            try:
                price = float(price_input)
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                menu.add_item(meal_type, name, price)
            except ValueError as e:
                print(f"Invalid price: {e}")
        elif choice == '3':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
                print("Invalid meal type.")
                continue
            menu.view_menu()
            try:
                index = int(input("Enter item index to remove: ")) - 1
                menu.remove_item(meal_type, index)
            except ValueError:
                print("Invalid index input. Please enter a valid number.")
        elif choice == '4':
            meal_type = input("Enter meal type: ").strip().lower()
            if meal_type not in Menu.MEAL_TYPES:
                print("Invalid meal type.")
                continue
            menu.view_menu()
            try:
                index = int(input("Enter item index to update: ")) - 1
                name = input("Enter new item name (or leave blank for no change): ").strip()
                price_input = input("Enter new item price (or leave blank for no change): ").strip()
                
                new_name = name if name else None
                new_price = None
                if price_input:
                    new_price = float(price_input)
                    if new_price <= 0:
                        print("Price must be a positive number.")
                        continue
                
                menu.update_item(meal_type, index, new_name, new_price)
            except ValueError:
                print("Invalid input. Please enter a valid numeric index or a valid price.")
        elif choice == '5':
            print("Exiting the menu management system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

main()
