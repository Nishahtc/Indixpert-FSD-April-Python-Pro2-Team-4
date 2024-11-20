import logging
import os
# from datetime import datetime

LOG_FILE_PATH = "src/database/activity.log"

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_login(username, role):
    logging.info(f"{role.capitalize()} '{username}' logged in.")

def log_logout(username, role):
    logging.info(f"{role.capitalize()} '{username}' logged out.")

def log_order(username, customer_name, items, quantities, total_amount):
    items_str = ', '.join([f"{item} (x{qty})" for item, qty in zip(items, quantities)])
    logging.info(
        f"Order placed by '{username}' for customer '{customer_name}': Items - [{items_str}], Total Amount: {total_amount:.2f}"
    )

def log_error(message):
    logging.error(f"Error: {message}")
