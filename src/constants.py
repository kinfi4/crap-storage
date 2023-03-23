import re

# Constants for UI

WINDOW_SIZE = "1200x800"

CUSTOMERS_COLUMNS = ("_id", "full_name", "email")
CUSTOMER_COLUMNS_SIZE = (25, 150, 200)

CUSTOMER_COLUMN_FULL = ("_id", "full_name", "email")
CUSTOMER_COLUMN_FULL_SIZE = (25, 120, 150, 90, 200, 35)

PRODUCTS_COLUMNS = ("_id", "name", "price", "description")
PRODUCT_COLUMNS_SIZE = (25, 120, 50, 50, 130)

ORDERS_COLUMNS = ("_id", "qty", "customer_id", "product_id")
ORDER_COLUMNS_SIZE = (25, 60, 60, 40, 200, 120)

BACKGROUND = "azure3"
FOREGROUND = "azure4"
ERROR_COLOR = "red"

EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")