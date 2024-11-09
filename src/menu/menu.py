import json
import os
from src.utility.validations import *

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
        print("\n--- MENU ---")
        for meal_type, items in self.menu_data.items():
            print(f"\n{meal_type.upper()}:")
            if not items:
                print("  No items available.")
            else:
                for index, item in enumerate(items, start=1):
                    print(f"  {index}. {item}")
    
    def get_item_price(self, item_name):
        for meal_type, items in self.menu_data.items():
            for item in items:
                if item.name.lower() == item_name.lower():
                    return item.price
        return None

    def add_item(self, meal_type, name, price):
        if meal_type not in self.MEAL_TYPES:
            print(f"Invalid meal type: {meal_type}.")
        if not validate_item(name):
            print("Invalid item name.")
        price = validate_price(price)
        if not price:
            print("Invalid price.")

        new_item = MenuItem(name, price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        print(f"Added to {meal_type}: {new_item}")

    def remove_item(self, meal_type, index):
        if meal_type not in self.MEAL_TYPES or index < 0 or index >= len(self.menu_data[meal_type]):
            print("Invalid index or meal type.")

        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        print(f"Removed from {meal_type}: {removed_item}")

    def manage_menu(self):
        try:
            while True:
                print("\n--- Menu Management ---")
                print("1. View Menu")
                print("2. Add Menu Item")
                print("3. Remove Menu Item")
                print("4. Go Back to Dashboard")

                choice = input("Choose an option: ")

                if choice == '1':
                    self.view_menu()
                    self.prompt_return_to_dashboard()
                elif choice == '2':
                    meal_type = menu(input("Enter meal type: "))
                    name = input("Enter item name: ").strip()
                    price = input("Enter item price: ").strip()
                    self.add_item(meal_type, name, price)
                elif choice == '3':
                    meal_type = input("Enter meal type: ").strip().lower()
                    self.view_menu()
                    try:
                        index = int(input("Enter item number to remove: ")) - 1
                        self.remove_item(meal_type, index)
                    except ValueError:
                        print("Invalid index.")
                elif choice == '4':
                    print("Returning to the main dashboard.")
                    break
                else:
                    print("Invalid choice.")
        except Exception as error:
            print(error)
            

    def prompt_return_to_dashboard(self):
        while True:
            print("\nEnter 'b' to go back to the main dashboard.")
            user_input = input("Enter choice: ").strip().lower()
            if user_input == 'b':
                break
            else:
                print("Invalid input. Please enter 'b' to go back.")
                