import json
import os
from src.utility.validation import validate_meal_type,validate_index,validate_price

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
            try:
                with open(self.file, 'r') as f:
                    menu_data = json.load(f)
                return {meal: [MenuItem.from_dict(item) for item in items] for meal, items in menu_data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                print("Error loading menu. Initializing empty menu.")

        return {meal: [] for meal in self.MEAL_TYPES}

    def save_menu(self):
        with open(self.file, 'w') as file:
            json.dump({meal: [item.__dict__ for item in items] for meal, items in self.menu_data.items()}, file, indent=4)
        print("Menu saved successfully.")  # Debugging print

    def view_menu(self):
        print("\n" + "*" * 30 + " MENU " + "*" * 30)
        for meal_type, items in self.menu_data.items():
            print(f"\n{'*' * 10}{meal_type.upper()}{'*' * 10}")
            if not items:
                print("  No items available.")
            else:
                print(f"\n{'S No.':<10}{'NAME':<30}{'PRICE':<10}")
                print("-" * 50)
                for index, item in enumerate(items):
                    print(f"{index + 1:<10}{item.name:<30}{item.price:<10.2f}")
        print("\n" + "*" * 60)

    def add_item(self, meal_type, name, price_input):
        validate_meal_type(meal_type, self.MEAL_TYPES)
        price = validate_price(price_input)
        new_item = MenuItem(name, price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        return f"Added to {meal_type}: {new_item}"

    def remove_item(self, meal_type, index_input):
        validate_meal_type(meal_type, self.MEAL_TYPES)
        index = validate_index(index_input, len(self.menu_data[meal_type]))
        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        return f"Removed from {meal_type}: {removed_item}"

    def update_item(self, meal_type, index_input, name, price_input):
        validate_meal_type(meal_type, self.MEAL_TYPES)
        index = validate_index(index_input, len(self.menu_data[meal_type]))

        item = self.menu_data[meal_type][index]
        if name:
            item.name = name
        if price_input:
            item.price = validate_price(price_input)
        self.save_menu()
        return f"Updated item in {meal_type}: {item}"

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
            try:
                meal_type = input("Enter meal type: ").strip().lower()
                name = input("Enter item name: ").strip()
                price_input = input("Enter item price: ").strip()
                print(menu.add_item(meal_type, name, price_input))
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                meal_type = input("Enter meal type: ").strip().lower()
                menu.view_menu()
                index_input = input("Enter item index to remove: ")
                print(menu.remove_item(meal_type, index_input))
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            try:
                meal_type = input("Enter meal type: ").strip().lower()
                menu.view_menu()
                index_input = input("Enter item index to update: ")
                name = input("Enter new item name (leave blank to keep): ").strip()
                price_input = input("Enter new price (leave blank to keep): ").strip()
                print(menu.update_item(meal_type, index_input, name, price_input))
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

main()
