-- 1. Count all orders, including orders without items.
SELECT COUNT(*) AS total_orders
FROM orders;

-- 2. Count orders in each recorded status.
SELECT order_status, COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC, order_status;

-- 3. Sum item prices on delivered orders, excluding freight.
SELECT ROUND(SUM(i.price), 2) AS total_sales_value_brl
FROM order_items AS i
INNER JOIN orders AS o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered';

-- 4. Divide sales by the number of distinct delivered orders with items.
SELECT ROUND(SUM(i.price) / COUNT(DISTINCT i.order_id), 2) AS average_order_value_brl
FROM order_items AS i
INNER JOIN orders AS o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered';

-- 5. Group delivered sales by purchase month (YYYY-MM).
SELECT STRFTIME('%Y-%m', o.order_purchase_timestamp) AS purchase_month,
       ROUND(SUM(i.price), 2) AS sales_value_brl
FROM order_items AS i
INNER JOIN orders AS o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY purchase_month
ORDER BY purchase_month;

-- 6. Rank categories by delivered sales value, keeping items with missing categories.
SELECT COALESCE(t.product_category_name_english, p.product_category_name, 'Uncategorized') AS category,
       ROUND(SUM(i.price), 2) AS sales_value_brl
FROM order_items AS i
INNER JOIN orders AS o ON i.order_id = o.order_id
INNER JOIN products AS p ON i.product_id = p.product_id
LEFT JOIN category_translation AS t ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY sales_value_brl DESC, category
LIMIT 10;

-- 7. Rank categories by the number of delivered item rows.
SELECT COALESCE(t.product_category_name_english, p.product_category_name, 'Uncategorized') AS category,
       COUNT(*) AS items_sold
FROM order_items AS i
INNER JOIN orders AS o ON i.order_id = o.order_id
INNER JOIN products AS p ON i.product_id = p.product_id
LEFT JOIN category_translation AS t ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY items_sold DESC, category
LIMIT 10;

-- 8. Rank customer states by order count across all statuses.
SELECT c.customer_state, COUNT(*) AS order_count
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY order_count DESC, c.customer_state
LIMIT 10;

-- 9. Count items per delivered order with items, then average those counts.
WITH items_per_order AS (
    SELECT i.order_id, COUNT(*) AS item_count
    FROM order_items AS i
    INNER JOIN orders AS o ON i.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY i.order_id
)
SELECT ROUND(AVG(item_count), 2) AS average_items_per_order
FROM items_per_order;

-- 10. Compare each month with delivered sales to the average of those months.
WITH monthly_sales AS (
    SELECT STRFTIME('%Y-%m', o.order_purchase_timestamp) AS purchase_month,
           SUM(i.price) AS sales_value_brl
    FROM order_items AS i
    INNER JOIN orders AS o ON i.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY purchase_month
)
SELECT purchase_month, ROUND(sales_value_brl, 2) AS sales_value_brl
FROM monthly_sales
WHERE sales_value_brl > (SELECT AVG(sales_value_brl) FROM monthly_sales)
ORDER BY purchase_month;
