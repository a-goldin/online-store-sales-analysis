# Исходные данные

[English](README.md) · [Русский](README.ru.md)

В проекте используется [открытый датасет Olist о бразильской электронной торговле](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Скачайте архив с Kaggle и распакуйте пять файлов из таблицы ниже в папку `data/`. Сохраните исходные имена и содержимое. CSV исключены из Git.

| Файл | Что означает одна строка | Ключ | Проверено строк |
| --- | --- | --- | ---: |
| `olist_orders_dataset.csv` | Заказ | `order_id` | 99 441 |
| `olist_order_items_dataset.csv` | Товарная позиция в заказе | `order_id` + `order_item_id` | 112 650 |
| `olist_customers_dataset.csv` | Запись о покупателе, связанная с заказом | `customer_id` | 99 441 |
| `olist_products_dataset.csv` | Товар | `product_id` | 32 951 |
| `product_category_name_translation.csv` | Перевод названия категории | `product_category_name` | 71 |

Все пять ключей заполнены и уникальны. Каждая позиция связана с заказом и товаром, у каждого заказа есть запись о покупателе. У 775 заказов нет товарных позиций. Во всех доставленных заказах есть позиции. Поля `price`, `order_purchase_timestamp` и `customer_state` заполнены.

У 610 товаров категория не указана. Для двух категорий нет английского перевода: `pc_gamer` и `portateis_cozinha_e_preparadores_de_alimentos`. Если перевода нет, используем исходное название. Если исходная категория пуста, используем `Uncategorized`.
