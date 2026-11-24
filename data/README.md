# Source data

[English](README.md) · [Русский](README.ru.md)

The project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Download the archive from Kaggle and extract the following five CSV files into `data/`. Keep their original names and contents. Git ignores the source CSVs so the repository can be published without bundling the dataset.

| File | One row represents | Key | Rows verified |
| --- | --- | --- | ---: |
| `olist_orders_dataset.csv` | An order | `order_id` | 99,441 |
| `olist_order_items_dataset.csv` | An item in an order | `order_id` + `order_item_id` | 112,650 |
| `olist_customers_dataset.csv` | A customer record linked to an order | `customer_id` | 99,441 |
| `olist_products_dataset.csv` | A product | `product_id` | 32,951 |
| `product_category_name_translation.csv` | A category translation | `product_category_name` | 71 |

The five keys are complete and unique. Every item matches an order and a product, and every order matches a customer. There are 775 orders without items. The delivered orders all have items. The `price`, `order_purchase_timestamp`, and `customer_state` fields are complete.

There are 610 product records with missing category names. Two category names have no English translation: `pc_gamer` and `portateis_cozinha_e_preparadores_de_alimentos`. Preserve existing category names when the translation is missing. Use `Uncategorized` as the display label when the source category is blank.
