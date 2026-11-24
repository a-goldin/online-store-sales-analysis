# SQLite analysis

From the project root, run:

```powershell
python sql/create_database.py
```

Python uses its built-in `sqlite3` module. The script reads the five CSVs from `data/` and creates `sql/ecommerce.db`. Run it again to rebuild the database from scratch. Close any open database viewer before rebuilding.

Open `ecommerce.db` in a SQLite client and run the statements in `sales_queries.sql` individually to see all ten results. If you already have the SQLite command-line tool, you can run the whole file from the project root:

```powershell
sqlite3 -header -column sql/ecommerce.db ".read sql/sales_queries.sql"
```

## How the counts work

- **Queries 1, 2 and 8.** One row in `orders` represents one order. Joining to `customers` via the unique `customer_id` adds the buyer's state while preserving that row count.
- **Queries 3–7.** One row in `order_items` represents a single item in an order. Sum `price` for delivered sales in BRL. Use `COUNT(DISTINCT order_id)` for the average order value denominator because an order can span multiple rows.
- **Queries 6 and 7.** The translation join keeps every item. `COALESCE` uses the English title first, then the original title, then `Uncategorized`.
- **Queries 9 and 10.** A `WITH` clause names an intermediate result. Query 9 builds one row per delivered order with items before taking the average. Query 10 builds one row per purchase month with delivered sales before comparing it with the average monthly sales value.
