# Power BI measures

Create these measures in the `Sales` table. The CSV contains one row per delivered item and excludes freight from `ItemPrice`. The same measures respond to the date, state and category filters on the report.

```dax
Total Sales Value = SUM(Sales[ItemPrice])
```

```dax
Total Orders = DISTINCTCOUNT(Sales[OrderID])
```

```dax
Average Order Value = DIVIDE([Total Sales Value], [Total Orders])
```

```dax
Unique Customers = DISTINCTCOUNT(Sales[CustomerID])
```

```dax
Total Items Sold = COUNTROWS(Sales)
```

```dax
Average Item Price = DIVIDE([Total Sales Value], [Total Items Sold])
```

```dax
Product Categories =
CALCULATE(
    DISTINCTCOUNT(Sales[Category]),
    KEEPFILTERS(Sales[Category] <> "Uncategorized")
)
```

```dax
Category Share =
DIVIDE(
    [Total Sales Value],
    CALCULATE([Total Sales Value], ALLSELECTED(Sales[Category]))
)
```

Use whole numbers for counts, two decimals for amounts in BRL, and one decimal place for Category Share. The categories KPI excludes the display bucket `Uncategorized`. Those items still contribute to sales and item counts. Category Share divides a category's sales by sales in the current selection. Selecting just one category makes its share 100%.

With a category selected, average order value uses the value of matching items and the count of orders containing those items. An order can contribute to multiple category counts, so use the distinct count measure for the overall total.
