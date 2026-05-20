# 📈 Sales Performance Dashboard

This project provides a complete sales data engineering and dashboard pipeline. It generates multi-year transactional sales records with embedded seasonal trends and processes them to output executive KPIs, performance summaries, and visualization charts.

## 🎯 Objectives
- Track key sales performance indicators (KPIs) like Revenue, Net Profit, and Profit Margins.
- Analyze monthly sales trends to identify seasonality.
- Group sales by Region and Product Category to find high-performing dimensions.
- Build both static executive reports (PNG) and interactive web dashboards (HTML).

## 🛠️ Tech Stack
- **Data Ingestion & Processing**: Python, Pandas, Numpy
- **Data Visualization**: Matplotlib, Seaborn, Plotly
- **Business Intelligence**: Power BI (Integration ready)

## 📋 Data Schema
The generated file `sales_data.csv` contains the following fields:
- `Transaction_ID`: Unique transactional string.
- `Date`: Transaction date (YYYY-MM-DD).
- `Customer_Segment`: Consumer, Corporate, or Home Office.
- `Region`: North, South, East, West.
- `City`: City name.
- `Product_Category`: Electronics, Fashion, Home & Kitchen, Sports & Outdoors.
- `Product_Name`: Item name.
- `Units_Sold`: Quantity purchased.
- `Unit_Price`: Sales price per unit.
- `Cost_Price`: Manufacturing/Wholesale cost per unit.
- `Discount_Pct`: Applied discount (0% - 20%).
- `Revenue`: Final sales revenue (Units * Price * (1 - Discount)).
- `Cost`: Total product cost (Units * Cost Price).
- `Profit`: Net profit (Revenue - Cost).

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic sales transaction dataset:
   ```bash
   python generate_data.py
   ```
3. Run the analytical pipeline and dashboard generator:
   ```bash
   python analysis.py
   ```

## 📊 Deliverables
- `sales_data.csv`: Clean tabular dataset prepared for database injection or BI analysis.
- `sales_performance_summary.csv`: Aggregated total KPIs.
- `visualizations/sales_kpi_dashboard.png`: Executive 4-panel report dashboard.
- `visualizations/interactive_sales_dashboard.html`: Dynamic HTML dashboard (opens in any browser with interactive filters and hover effects).

---

## 🖥️ Power BI Integration Guide
To build a dashboard in Power BI Desktop using this project:

1. **Load Data**:
   - Open Power BI Desktop.
   - Click on **Get Data** -> **Text/CSV**.
   - Select `sales_data.csv` and click **Load**.

2. **Define Key Measures (DAX)**:
   - Create a table for Measures and define the following key metrics:
     - `Total Revenue = SUM(sales_data[Revenue])`
     - `Total Profit = SUM(sales_data[Profit])`
     - `Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100`
     - `Average Order Value = AVERAGE(sales_data[Revenue])`

3. **Build the Visuals**:
   - **KPI Cards**: Place three Card visuals at the top for `Total Revenue`, `Total Profit`, and `Profit Margin %`.
   - **Line Chart**: Drag `Date` (Month) to Axis and `Revenue` to Values to show Sales Trends.
   - **Stacked Bar Chart**: Drag `Region` to Axis, and `Revenue` & `Profit` to Values to analyze Regional Performance.
   - **Donut Chart**: Drag `Product_Category` to Legend and `Revenue` to Values.
   - **Slicers**: Add slicers for `Customer_Segment` and `Region` for interactive filtering.
