"""Build the local SQLite database from the five original Olist CSV files."""

import csv
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


SQL_DIR = Path(__file__).resolve().parent
DATA_DIR = SQL_DIR.parent / "data"
DATABASE = SQL_DIR / "ecommerce.db"

# Load parent tables before the tables that reference them.
SOURCE_FILES = {
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
}

SCHEMA = """
CREATE TABLE customers (
    customer_id TEXT NOT NULL PRIMARY KEY,
    customer_unique_id TEXT NOT NULL,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT NOT NULL
);

CREATE TABLE products (
    product_id TEXT NOT NULL PRIMARY KEY,
    product_category_name TEXT,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER
);

CREATE TABLE category_translation (
    product_category_name TEXT NOT NULL PRIMARY KEY,
    product_category_name_english TEXT NOT NULL
);

CREATE TABLE orders (
    order_id TEXT NOT NULL PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    order_status TEXT NOT NULL,
    order_purchase_timestamp TEXT NOT NULL,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT
);

CREATE TABLE order_items (
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    order_item_id INTEGER NOT NULL,
    product_id TEXT NOT NULL REFERENCES products(product_id),
    seller_id TEXT,
    shipping_limit_date TEXT,
    price REAL NOT NULL,
    freight_value REAL,
    PRIMARY KEY (order_id, order_item_id)
);
"""


def load_csv(connection, table, path):
    # Read columns in schema order and bind CSV values as SQL parameters.
    columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
    placeholders = ", ".join("?" for _ in columns)
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if len(reader.fieldnames or []) != len(columns) or set(reader.fieldnames) != set(columns):
            raise ValueError(f"Unexpected columns in {path.name}")
        rows = (tuple(row[column] or None for column in columns) for row in reader)
        result = connection.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
        return result.rowcount


def main():
    missing = [name for name in SOURCE_FILES.values() if not (DATA_DIR / name).is_file()]
    if missing:
        raise SystemExit("Missing files in data/: " + ", ".join(missing))

    # Publish the database only after every CSV has loaded successfully.
    with TemporaryDirectory(dir=SQL_DIR) as temporary_dir:
        temporary_database = Path(temporary_dir) / DATABASE.name
        with closing(sqlite3.connect(temporary_database)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(SCHEMA)
            with connection:
                for table, filename in SOURCE_FILES.items():
                    count = load_csv(connection, table, DATA_DIR / filename)
                    print(f"{table}: {count:,} rows")
        temporary_database.replace(DATABASE)
    print(f"Database ready: {DATABASE}")


if __name__ == "__main__":
    main()
