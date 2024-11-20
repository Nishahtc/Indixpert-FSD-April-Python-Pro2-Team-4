import os
import json
from datetime import datetime, timedelta

DATABASE_FOLDER = "src/database"
ORDERS_FILE = os.path.join(DATABASE_FOLDER, "order.json")
REPORT_FILE = os.path.join(DATABASE_FOLDER, "sales_report.txt")


class Reports:
    @staticmethod
    def load_orders():
        if os.path.exists(ORDERS_FILE):
            try:
                with open(ORDERS_FILE, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: Unable to read orders file. Invalid JSON format.")
        return []

    @staticmethod
    def filter_orders_by_date(orders, start_date, end_date):
        filtered_orders = []
        for order in orders:
            order_date = datetime.strptime(order['order_date'], "%Y-%m-%d %H:%M:%S")
            if start_date <= order_date <= end_date:
                filtered_orders.append(order)
        return filtered_orders

    @staticmethod
    def generate_sales_report():
        orders = Reports.load_orders()
        if not orders:
            print("No orders found for the report.")
            return None, None

        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_week_start = now - timedelta(days=7)

        weekly_orders = Reports.filter_orders_by_date(orders, last_week_start, now)
        daily_orders = Reports.filter_orders_by_date(orders, today_start, now)

        weekly_total = sum(order['total_amount'] for order in weekly_orders)
        daily_total = sum(order['total_amount'] for order in daily_orders)

        report_content = "\n" + "=" * 60 + "\n"
        report_content += f"{'Sales Report':^60}\n"
        report_content += "=" * 60 + "\n"
        report_content += f"Report Generated On: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_content += "=" * 60 + "\n\n"

        # Weekly Sales Report
        report_content += f"{'Weekly Sales Report (Last 7 Days)':^60}\n"
        report_content += "-" * 60 + "\n"
        report_content += f"{'Total Weekly Sales':<30}: {int(weekly_total):>10}\n"
        report_content += "\nDetailed Orders:\n"
        for order in weekly_orders:
            report_content += "-" * 60 + "\n"
            report_content += f"Order ID      : {order['id']}\n"
            report_content += f"Customer Name : {order['customer_name']}\n"
            report_content += f"Table Number  : {order.get('table_number', 'N/A')}\n"
            report_content += f"Total Amount  : {int(order['total_amount']):}\n"
            report_content += f"Order Date    : {order['order_date']}\n"

        report_content += "\n" + "=" * 60 + "\n\n"

        # Today's Sales Report
        report_content += f"{'Today\'s Sales Report':^60}\n"
        report_content += "-" * 60 + "\n"
        report_content += f"{'Total Daily Sales':<30}: {int(daily_total):>10}\n"
        report_content += "\nDetailed Orders:\n"
        for order in daily_orders:
            report_content += "-" * 60 + "\n"
            report_content += f"Order ID      : {order['id']}\n"
            report_content += f"Customer Name : {order['customer_name']}\n"
            report_content += f"Table Number  : {order.get('table_number', 'N/A')}\n"
            report_content += f"Total Amount  : {int(order['total_amount']):}\n"
            report_content += f"Order Date    : {order['order_date']}\n"

        report_content += "\n" + "=" * 60 + "\n"

        with open(REPORT_FILE, 'w') as file:
            file.write(report_content)

        print("Sales report has been generated successfully.")
        return weekly_total, daily_total
