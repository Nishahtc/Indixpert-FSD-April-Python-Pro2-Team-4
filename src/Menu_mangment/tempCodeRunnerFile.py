 # def add_item(self, meal_type, name, price_input):
    #     print(f"Adding item to {meal_type}: {name} at {price_input}")  # Debugging print
    #     validate_meal_type(meal_type, self.MEAL_TYPES)
    #     price = validate_price(price_input)
    #     new_item = MenuItem(name, price)
    #     self.menu_data[meal_type].append(new_item)
    #     self.save_menu()
    #     return f"Added to {meal_type}: {new_item}"

    # def remove_item(self, meal_type, index_input):
    #     print(f"Removing item from {meal_type} at index {index_input}")  # Debugging print
    #     validate_meal_type(meal_type, self.MEAL_TYPES)
    #     index = validate_index(index_input, len(self.menu_data[meal_type]))
    #     removed_item = self.menu_data[meal_type].pop(index)
    #     self.save_menu()
    #     return f"Removed from {meal_type}: {removed_item}"

    # def update_item(self, meal_type, index_input, name, price_input):
    #     print(f"Updating item in {meal_type} at index {index_input}")  # Debugging print
    #     validate_meal_type(meal_type, self.MEAL_TYPES)
    #     index = validate_index(index_input, len(self.menu_data[meal_type]))

    #     item = self.menu_data[meal_type][index]
    #     if name:
    #         item.name = name
    #     if price_input:
    #         price = validate_price(price_input)
    #         item.price = price
    #     self.save_menu()
    #     return f"Updated item in {meal_type}: {item}"