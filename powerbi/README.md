# Power BI report

Open `sales_dashboard.pbix` in Power BI Desktop. The file includes an imported copy of the data and opens with the full delivered-order period selected.

## Refresh on another computer

From the project root, run the following commands after placing the five Olist CSV files in `data/`.

```powershell
python sql/create_database.py
python powerbi/prepare_data.py
```

In Power BI Desktop, open **Transform data → Edit parameters**, enter the full path to the generated `powerbi/sales.csv` as `SalesCsvPath`, and apply the change. Refresh the report. The query imports UTF-8, uses the purchase date in `OrderDate`, and parses `ItemPrice` as a fixed decimal in BRL.

## Explore the pages

| Page | Filters | What to look for |
| --- | --- | --- |
| Sales Overview | Purchase date and customer state | Four KPI cards, monthly merchandise sales, top ten categories by sales, and sales by customer state |
| Product Analysis | Purchase date and product category | Three KPI cards, category rankings by items and sales, category share, and monthly sales for the selected categories |

In Product Analysis, choose a category in the slicer to filter the whole page. Select a category in a ranking or the treemap to filter the monthly trend. Hover over a treemap rectangle to see its share of sales in the current selection.

The report uses one table with one row per delivered item. It counts distinct `OrderID` values for orders and distinct `CustomerID` values for customers. All-order counts and the order-status distribution are available in the SQL, Pandas and Excel analyses. See [Power BI measures](measures.md) for the DAX definitions.

## Reconciliation values

| Selection | Sales (BRL) | Orders | Average order value (BRL) | Unique customers | Items | Average item price (BRL) | Known categories |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All | 13,221,498.11 | 96,478 | 137.04 | 93,358 | 110,197 | 119.98 | 73 |
| State AC | 15,930.97 | 80 | 199.14 | 76 | 91 | 175.07 | 27 |
| Category `agro_industry_and_commerce` | 70,566.10 | 177 | 398.68 | 176 | 206 | 342.55 | 1 |
| Same category, from August 20, 2017 | 66,043.36 | 160 | 412.77 | 160 | 188 | 351.29 | 1 |
