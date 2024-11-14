import json
import os
from src.utility.validations import *
from src.utility.messages import Messages

DATABASE_FOLDER = "src/database"
MENU_FILE_PATH = os.path.join(DATABASE_FOLDER, "menu.json")

class MenuItem:
    def __init__(self, name, full_price, half_price):
        self.name = name
        self.full_price = full_price
        self.half_price = half_price

    def __str__(self):
        if self.half_price is not None:
            return f"{self.name}: Full Price - {self.full_price}, Half Price - {self.half_price}"
        else:
            return f"{self.name}: Full Price - {self.full_price}"

    @classmethod
    def from_dict(cls, item_dict):
        name = item_dict['name']
        full_price = item_dict['full_price']
        half_price = item_dict.get('half_price')
        return cls(name, full_price, half_price)

class Menu:
    MEAL_TYPES = [
        "breakfast", "lunch", "dinner", "snacks", 
        "soups", "starters", "main_course", "noodles",
        "rice", "desserts", "extras", "tea_and_coffee", "aerated_beverages", "ice_cream"
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
                    Messages.error_loading_menu()
                    print(f"Error: Menu file '{self.file}' is corrupted. Loading empty menu.")
        return {meal: [] for meal in self.MEAL_TYPES}
    
    def get_item_price(self, item_name, portion_size):
        for items in self.menu_data.values():
            for item in items:
                if item.name.lower() == item_name.lower():
                    if portion_size == 'full':
                        return item.full_price
                    elif portion_size == 'half' and item.half_price is not None:
                        return item.half_price
        return None

    def save_menu(self):
        with open(self.file, 'w') as file:
            json.dump({meal: [item.__dict__ for item in items] for meal, items in self.menu_data.items()}, file, indent=4)

    def view_menu(self):
        border = "=" * 55
        print(border)
        print(f"{'RESTAURANT MENU':^55}")
        print(border)
        
        for meal_type, items in self.menu_data.items():
            print(f"\n{meal_type.upper():^55}")
            print("-" * 55)
            
            if not items:
                print(f"{'No items available':^55}")
            else:
                print(f"{'S.No':<5}{'Item Name':<25}{'Full Price':>10}  {'Half Price':>10}")
                print("-" * 55)
                for index, item in enumerate(items, start=1):
                    full_price = f"{item.full_price}"
                    half_price = f"{item.half_price}" if item.half_price is not None else "N/A"
                    print(f"{index:<5}{item.name:<25}{full_price:>10}{half_price:>10}")
        print(border)

    def add_item(self, meal_type, name, full_price, half_price):
        if meal_type not in self.MEAL_TYPES:
            Messages.invalid_meal_type(meal_type)
            return

        if any(item.name.lower() == name.lower() for item in self.menu_data[meal_type]):
            Messages.item_already_exists(name)
            return

        new_item = MenuItem(name, full_price, half_price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        Messages.item_added(meal_type, new_item)

    def handle_add_item(self):
        search = input("Enter meal type initial: ").strip().lower()
        matching_meals = self.search_meal_type(search)

        if not matching_meals:
            print(f"No meal types found starting with '{search}'")
            return

        if len(matching_meals) > 1:
            print(f"Matching meal types: {', '.join(matching_meals)}")
            meal_type = input("Enter the full meal type from the list above: ").strip().lower()
            if meal_type not in matching_meals:
                Messages.invalid_meal_type(meal_type)
                return
        else:
            meal_type = matching_meals[0]

     
        name = input(Messages.enter_item_name()).strip()
        if not validate_item(name):
            Messages.invalid_item_name()
            return

        try:
            full_price = float(input(Messages.enter_item_price()).strip())
            half_price_input = input("Enter half price : ").strip()
            half_price = float(half_price_input) if half_price_input else None
        except ValueError:
            Messages.invalid_price()
            return

        self.add_item(meal_type, name, full_price, half_price)

    def handle_remove_item(self):
        search = input("Enter meal type initial: ").strip().lower()
        matching_meals = self.search_meal_type(search)

        if not matching_meals:
            print(f"No meal types found starting with '{search}'")
            return

        if len(matching_meals) > 1:
            print(f"Matching meal types: {', '.join(matching_meals)}")
            meal_type = input("Enter the full meal type from the list above: ").strip().lower()
            if meal_type not in matching_meals:
                Messages.invalid_meal_type(meal_type)
                return
        else:
            meal_type = matching_meals[0]

        items = self.menu_data[meal_type]

        if not items:
            print(f"No items available under {meal_type.title()}.")
            return

        print(f"\n{meal_type.upper()} Items:")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item.name} (Full Price: {item.full_price}, Half Price: {item.half_price or 'N/A'})")

        try:
            item_index = int(input("Enter the item number to remove: ").strip()) - 1
            if item_index < 0 or item_index >= len(items):
                Messages.invalid_choice()
                return

            item_to_remove = items[item_index]
            confirm = input(f"Are you sure you want to remove '{item_to_remove.name}'? (yes/no): ").strip().lower()
            if confirm != 'yes':
                Messages.operation_cancelled()
                return

            del items[item_index]
            self.save_menu()
            Messages.item_removed(meal_type, item_to_remove.name)
        except ValueError:
            Messages.invalid_choice()

    def search_meal_type(self, initial):
        initial = initial.lower()
        return [meal for meal in self.MEAL_TYPES if meal.startswith(initial)]

    def manage_menu(self, user_role):
        try:
            while True:
                if user_role == 'staff':
                    self.view_menu()
                    self.prompt_return_to_dashboard()
                    break
                
                Messages.menu_management_menu()

                choice = input(Messages.enter_choice()).strip()

                if choice == '1':
                    self.view_menu()
                    self.prompt_return_to_dashboard()
                elif choice == '2':
                    self.handle_add_item()
                elif choice == '3':
                    self.handle_remove_item()
                elif choice == "4":
                    Messages.returning_to_dashboard()
                    break
                else:
                    Messages.invalid_choice()
        except Exception as error:
            Messages.error_message(error)

    def prompt_return_to_dashboard(self):
        while True:
            Messages.prompt_return()
            user_input = input(Messages.enter_choice()).strip().lower()
            if user_input == 'b':
                break
            else:
                Messages.invalid_input_b()