# Меры Power BI

[English](measures.md) · [Русский](measures.ru.md)

Меры принадлежат таблице `Sales`. Одна строка CSV соответствует одной доставленной позиции. `ItemPrice` содержит цену товара без стоимости доставки. Срезы по дате, штату и категории влияют на значения мер.

| Мера | Что считает |
| --- | --- |
| `Total Sales Value` | Сумму цен доставленных позиций |
| `Total Orders` | Число уникальных доставленных заказов в выборке |
| `Average Order Value` | Стоимость товаров в выборке, делённую на число уникальных заказов в этой выборке |
| `Unique Customers` | Число уникальных покупателей |
| `Total Items Sold` | Число строк с доставленными товарными позициями |
| `Average Item Price` | Стоимость товаров, делённую на число позиций |
| `Product Categories` | Число известных категорий в выборке |
| `Category Share` | Долю категории в стоимости товаров по текущей выборке |

```dax
Total Sales Value = SUM(Sales[ItemPrice])
Total Orders = DISTINCTCOUNT(Sales[OrderID])
Average Order Value = DIVIDE([Total Sales Value], [Total Orders])
Unique Customers = DISTINCTCOUNT(Sales[CustomerID])
Total Items Sold = COUNTROWS(Sales)
Average Item Price = DIVIDE([Total Sales Value], [Total Items Sold])

Product Categories =
CALCULATE(
    DISTINCTCOUNT(Sales[Category]),
    KEEPFILTERS(Sales[Category] <> "Uncategorized")
)

Category Share =
DIVIDE(
    [Total Sales Value],
    CALCULATE([Total Sales Value], ALLSELECTED(Sales[Category]))
)
```

Количество отображается целыми числами, денежные показатели в BRL с двумя знаками после запятой, доля категории с одним. В счётчик известных категорий `Uncategorized` не входит. Позиции с этой меткой участвуют в расчёте стоимости и количества товаров.

При выборе одной категории её доля в текущей выборке составляет 100%. Средний чек при таком выборе делит стоимость выбранных товаров на число заказов, в которых они были. Один заказ с товарами из разных категорий может учитываться в каждой из них, поэтому общий итог заново считает уникальные заказы.
