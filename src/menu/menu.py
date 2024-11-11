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
            return f"{self.name}: Full Price - {self.full_price:.2f}, Half Price - {self.half_price:.2f}"
        else:
            return f"{self.name}: Full Price - {self.full_price:.2f}"

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
                    Messages.error_loading_menu()
        return {meal: [] for meal in self.MEAL_TYPES}

    def save_menu(self):
        with open(self.file, 'w') as file:
            json.dump({meal: [item.__dict__ for item in items] for meal, items in self.menu_data.items()}, file, indent=4)

    def view_menu(self):
        border = "=" * 50
        print(border)
        print(f"{'RESTAURANT MENU':^50}")
        print(border)
        
        for meal_type, items in self.menu_data.items():
            print(f"\n{meal_type.upper():^50}")
            print("-" * 50)
            
            if not items:
                print(f"{'No items available':^50}")
            else:
                print(f"{'S.No':<5}{'Item Name':<25}{'Full Price':>10}{'Half Price':>10}")
                print("-" * 50)
                for index, item in enumerate(items, start=1):
                    full_price = f"{item.full_price:.2f}"
                    half_price = f"{item.half_price:.2f}" if item.half_price is not None else "N/A"
                    print(f"{index:<5}{item.name:<25}{full_price:>10}{half_price:>10}")
        print(border)
    
    def get_item_price(self, item_name, portion_size):
        for meal_type, items in self.menu_data.items():
            for item in items:
                if item.name.lower() == item_name.lower():
                    if portion_size == 'full':
                        return item.full_price
                    elif portion_size == 'half' and item.half_price is not None:
                        return item.half_price
                    else:
                        return None
        return None

    def add_item(self, meal_type, name, full_price, half_price):
        if meal_type not in self.MEAL_TYPES:
            Messages.invalid_meal_type(meal_type)
            return
        if not validate_item(name):
            Messages.invalid_item_name()
            return
        full_price = validate_price(full_price)
        half_price = validate_price(half_price)
        if not full_price or not half_price:
            Messages.invalid_price()
            return

        new_item = MenuItem(name, full_price, half_price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        Messages.item_added(meal_type, new_item)

    def remove_item(self, meal_type, index):
        if meal_type not in self.MEAL_TYPES or index < 0 or index >= len(self.menu_data[meal_type]):
            Messages.invalid_index_or_meal_type()
            return

        removed_item = self.menu_data[meal_type].pop(index)
        self.save_menu()
        Messages.item_removed(meal_type, removed_item)

    def manage_menu(self):
        try:
            while True:
                Messages.menu_management_menu()

                choice = input(Messages.enter_choice())

                if choice == '1':
                    self.view_menu()
                    self.prompt_return_to_dashboard()
                elif choice == '2':
                    meal_type = validate_meal_type(input(Messages.enter_meal_type()))
                    if not meal_type or meal_type not in self.MEAL_TYPES:
                        Messages.invalid_meal_type("Invalid meal type")
                        continue
                    
                    name = input(Messages.enter_item_name()).strip()
                    full_price = input(Messages.enter_item_price()).strip()
                    half_price = input("Enter half price (or press Enter if not applicable): ").strip() or None
                    
                    if half_price is not None:
                        half_price = validate_price(half_price)
                        
                    full_price = validate_price(full_price)
                    
                    if not full_price:
                        Messages.invalid_price()
                        continue
                    
                    new_item = MenuItem(name, full_price, half_price)
                    self.menu_data[meal_type].append(new_item)
                    self.save_menu()
                    Messages.item_added(meal_type, new_item)
                    
                elif choice == '3':
                    meal_type = validate_meal_type(input(Messages.enter_meal_type()))
                    if not meal_type or meal_type not in self.MEAL_TYPES:
                        Messages.invalid_meal_type(meal_type)
                        continue
                    
                    self.view_menu()
                    try:
                        index = int(input("Enter item number to remove: ")) - 1
                        self.remove_item(meal_type, index)
                    except ValueError:
                        Messages.invalid_index()
                
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
                