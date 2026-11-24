"""Export one row per delivered item for the Power BI report."""

import csv
import sqlite3
from contextlib import closing
from pathlib import Path


FOLDER = Path(__file__).resolve().parent
DATABASE = FOLDER.parent / "sql" / "ecommerce.db"
SALES_CSV = FOLDER / "sales.csv"

SALES_QUERY = """
SELECT o.order_id AS OrderID,
       i.order_item_id AS OrderItemID,
       DATE(o.order_purchase_timestamp) AS OrderDate,
       DATE(o.order_purchase_timestamp, 'start of month') AS PurchaseMonth,
       c.customer_unique_id AS CustomerID,
       c.customer_state AS State,
       COALESCE(t.product_category_name_english, p.product_category_name, 'Uncategorized') AS Category,
       i.price AS ItemPrice
FROM order_items AS i
JOIN orders AS o ON o.order_id = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN products AS p ON p.product_id = i.product_id
LEFT JOIN category_translation AS t ON t.product_category_name = p.product_category_name
WHERE o.order_status = 'delivered'
ORDER BY o.order_purchase_timestamp, o.order_id, i.order_item_id
"""


def main():
    if not DATABASE.is_file():
        raise SystemExit("Run python sql/create_database.py from the project root first.")

    with closing(sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True)) as db:
        cursor = db.execute(SALES_QUERY)
        headers = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        expected_items, expected_sales = db.execute("""
            SELECT COUNT(*), ROUND(SUM(i.price), 2)
            FROM order_items AS i JOIN orders AS o ON o.order_id = i.order_id
            WHERE o.order_status = 'delivered'
        """).fetchone()
        expected_orders = db.execute("""
            SELECT COUNT(*) FROM orders WHERE order_status = 'delivered'
        """).fetchone()[0]

    if len(rows) != expected_items or len({(row[0], row[1]) for row in rows}) != expected_items:
        raise ValueError("The export must contain each delivered item exactly once.")
    if len({row[0] for row in rows}) != expected_orders:
        raise ValueError("The item-level model requires at least one item in every delivered order.")
    if round(sum(row[-1] for row in rows), 2) != expected_sales:
        raise ValueError("The export total does not match the delivered item prices in SQLite.")

    with SALES_CSV.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Exported {len(rows):,} delivered item rows to {SALES_CSV}")


if __name__ == "__main__":
    main()
