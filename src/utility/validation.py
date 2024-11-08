def validate_meal_type(meal_type, valid_meal_types):
    """
    Validates if the meal_type is in the list of valid meal types.
    """
    if meal_type not in valid_meal_types:
        raise ValueError(f"Invalid meal type: {meal_type}. Valid types are: {', '.join(valid_meal_types)}")


def validate_price(price_input):
    """
    Validates if the input price is a valid positive float.
    """
    try:
        price = float(price_input)
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        return price
    except ValueError:
        raise ValueError("Invalid price. Please enter a valid positive number.")


def validate_index(index_input, max_index):
    """
    Validates if the index input is a valid integer within the valid range.
    """
    try:
        index = int(index_input) - 1
        if index < 0 or index >= max_index:
            raise IndexError("Index out of range.")
        return index
    except ValueError:
        raise ValueError("Invalid index. Please enter a valid number.")
