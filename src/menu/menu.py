import json
import os
from src.utility.validations import *
from src.utility.messages import messages
from src.utility.color import bcolors

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
        "rice", "desserts", "tea_and_coffee", "aerated_beverages", "ice_cream"
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
                    print(messages.data_load_error)
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
        print(bcolors.colorize(f"{'RESTAURANT MENU':^55}",bcolors.LIGHT_GREEN))
        print(border)

        for meal_type, items in self.menu_data.items():
            print(bcolors.colorize(f"\n{meal_type.upper():^55}",bcolors.ORANGE))
            print("-" * 55)

            if not items:
                print(bcolors.colorize(f"{'No items available':^55}",bcolors.YELLOW_UNDERLINE))
            else:
                print(bcolors.colorize(f"{'S.No':<5}{'Item Name':<25}{'Full Price':>10}  {'Half Price':>10}",bcolors.LIGHT_GREEN))
                print("-" * 55)
                for index, item in enumerate(items, start=1):
                    full_price = f"{item.full_price}"
                    half_price = f"{item.half_price}" if item.half_price is not None else "N/A"
                    print(bcolors.colorize(f"{index:<5}{item.name:<25}{full_price:>10}{half_price:>10}",bcolors.CYAN))
        print(border)

    def add_item(self, meal_type, name, full_price, half_price):
        if meal_type not in self.MEAL_TYPES:
            print(messages.invalid_meal_type.format(meal_type))
            return

        if any(item.name.lower() == name.lower() for item in self.menu_data[meal_type]):
            print(messages.item_exists.format(name))
            return

        new_item = MenuItem(name, full_price, half_price)
        self.menu_data[meal_type].append(new_item)
        self.save_menu()
        print(bcolors.colorize(f"Added {new_item} to {meal_type}.",bcolors.YELLOW_UNDERLINE))

    def handle_add_item(self):
        search = input(bcolors.colorize("Enter meal type initial: ",bcolors.PINK)).strip().lower()
        matching_meals = self.search_meal_type(search)

        if not matching_meals:
            print(bcolors.colorize(f"No meal types found starting with '{search}'",bcolors.WHITE_BOLD))
            return

        if len(matching_meals) > 1:
            print(bcolors.colorize(f"Matching meal types: {', '.join(matching_meals)}",bcolors.LIGHT_GREEN))
            meal_type = input(bcolors.colorize("Enter the full meal type from the list above: ",bcolors.PINK)).strip().lower()
        else:
            meal_type = matching_meals[0]

        name = input(bcolors.colorize("Enter item name: ",bcolors.PINK)).strip()
        if not validate_item(name):
            print(bcolors.colorize("Invalid item name.",bcolors.RED))
            return

        try:
            full_price = float(input(bcolors.colorize("Enter full price: ",bcolors.PINK)).strip())
            half_price_input = input(bcolors.colorize("Enter half price (leave blank if not applicable): ",bcolors.PINK)).strip()
            half_price = float(half_price_input) if half_price_input else None
        except ValueError:
            print(messages.invalid_input)
            return

        self.add_item(meal_type, name, full_price, half_price)

    def handle_remove_item(self):
        search = input(bcolors.colorize("Enter meal type initial: ",bcolors.PINK)).strip().lower()
        matching_meals = self.search_meal_type(search)

        if not matching_meals:
            print(bcolors.colorize(f"No meal types found starting with '{search}'",bcolors.YELLOW_UNDERLINE))
            return

        if len(matching_meals) > 1:
            print(bcolors.colorize(f"Matching meal types: {', '.join(matching_meals)}",bcolors.YELLOW_UNDERLINE))
            meal_type = input(bcolors.colorize("Enter the full meal type from the list above: ",bcolors.PINK)).strip().lower()
        else:
            meal_type = matching_meals[0]

        items = self.menu_data[meal_type]

        if not items:
            print(bcolors.colorize(f"No items available under {meal_type.title()}.",bcolors.YELLOW_UNDERLINE))
            return

        print(f"\n{meal_type.upper()} Items:")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item.name} (Full Price: {item.full_price}, Half Price: {item.half_price or 'N/A'})")

        try:
            item_index = int(input(bcolors.colorize("Enter the item number to remove: ",bcolors.PINK)).strip()) - 1
            if item_index < 0 or item_index >= len(items):
                print(messages.invalid_choice)
                return

            item_to_remove = items[item_index]
            confirm = input(bcolors.colorize(f"Are you sure you want to remove '{item_to_remove.name}'? (yes/no): ",bcolors.PINK)).strip().lower()
            if confirm != 'yes':
                print(bcolors.colorize("Operation cancelled.",bcolors.YELLOW_UNDERLINE))
                return

            del items[item_index]
            self.save_menu()
            print(bcolors.colorize(f"Removed {item_to_remove.name} from {meal_type}.",bcolors.YELLOW_UNDERLINE))
        except ValueError:
            print(messages.invalid_input)

    def search_meal_type(self, initial):
        initial = initial.lower()
        return [meal for meal in self.MEAL_TYPES if meal.startswith(initial)]
