import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("[*] Processing sales performance data...")
    csv_file = "sales_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.to_period('M')
    
    # Calculate key metrics
    total_revenue = df['Revenue'].sum()
    total_cost = df['Cost'].sum()
    total_profit = df['Profit'].sum()
    total_units = df['Units_Sold'].sum()
    avg_order_value = df['Revenue'].mean()
    overall_margin = (total_profit / total_revenue) * 100
    
    print("\n" + "="*30)
    print("      SALES PERFORMANCE KPIs")
    print("="*30)
    print(f"Total Revenue:   ${total_revenue:,.2f}")
    print(f"Total Profit:    ${total_profit:,.2f}")
    print(f"Profit Margin:   {overall_margin:.2f}%")
    print(f"Total Units:     {total_units:,}")
    print(f"Avg Order Value: ${avg_order_value:,.2f}")
    print("="*30)
    
    # Create visualizations folder
    os.makedirs("visualizations", exist_ok=True)
    
    # 1. Generate Static Dashboard using Matplotlib/Seaborn
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Sales Performance Executive Dashboard (2024 - 2025)', fontsize=18, fontweight='bold', color='#2c3e50')
    
    # Set Seaborn theme
    sns.set_theme(style="whitegrid")
    
    # Subplot 1: Monthly Sales Trend
    monthly_sales = df.groupby('Month_Year')['Revenue'].sum().reset_index()
    monthly_sales['Month_Year'] = monthly_sales['Month_Year'].astype(str)
    sns.lineplot(ax=axes[0, 0], data=monthly_sales, x='Month_Year', y='Revenue', marker='o', color='#1abc9c', linewidth=2.5)
    axes[0, 0].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold', color='#34495e')
    axes[0, 0].set_xticklabels(monthly_sales['Month_Year'], rotation=45, ha='right')
    axes[0, 0].set_xlabel('')
    axes[0, 0].set_ylabel('Revenue ($)')
    
    # Subplot 2: Region Performance (Revenue & Profit)
    region_perf = df.groupby('Region')[['Revenue', 'Profit']].sum().reset_index()
    region_melt = pd.melt(region_perf, id_vars=['Region'], value_vars=['Revenue', 'Profit'], 
                          var_name='Metric', value_name='Amount')
    sns.barplot(ax=axes[0, 1], data=region_melt, x='Region', y='Amount', hue='Metric', palette=['#3498db', '#e74c3c'])
    axes[0, 1].set_title('Revenue vs Profit by Region', fontsize=14, fontweight='bold', color='#34495e')
    axes[0, 1].set_xlabel('')
    axes[0, 1].set_ylabel('Amount ($)')
    
    # Subplot 3: Sales by Product Category
    cat_sales = df.groupby('Product_Category')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    colors = ['#34495e', '#3498db', '#2ecc71', '#9b59b6']
    axes[1, 0].pie(cat_sales['Revenue'], labels=cat_sales['Product_Category'], autopct='%1.1f%%', 
                   startangle=90, colors=colors, wedgeprops={'edgecolor': 'w', 'linewidth': 1})
    axes[1, 0].set_title('Revenue Distribution by Category', fontsize=14, fontweight='bold', color='#34495e')
    
    # Subplot 4: Top 5 Selling Products by Profit
    top_products = df.groupby('Product_Name')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False).head(5)
    sns.barplot(ax=axes[1, 1], data=top_products, y='Product_Name', x='Profit', palette='viridis')
    axes[1, 1].set_title('Top 5 Products by Net Profit', fontsize=14, fontweight='bold', color='#34495e')
    axes[1, 1].set_xlabel('Total Profit ($)')
    axes[1, 1].set_ylabel('')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("visualizations/sales_kpi_dashboard.png", dpi=150)
    plt.close()
    print("[+] Saved static dashboard to visualizations/sales_kpi_dashboard.png")
    
    # Try generating interactive Plotly dashboard if package is available
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import plotly.express as px
        
        print("[*] Plotly detected. Creating interactive dashboard...")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Monthly Revenue Trend", "Revenue & Profit by Region", 
                            "Category Sales Share", "Top 10 Products by Profit"),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "domain"}, {"type": "bar"}]]
        )
        
        # Trend
        fig.add_trace(
            go.Scatter(x=monthly_sales['Month_Year'], y=monthly_sales['Revenue'], 
                       mode='lines+markers', name='Revenue', line=dict(color='#1abc9c', width=3)),
            row=1, col=1
        )
        
        # Region
        fig.add_trace(
            go.Bar(x=region_perf['Region'], y=region_perf['Revenue'], name='Revenue', marker_color='#3498db'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=region_perf['Region'], y=region_perf['Profit'], name='Profit', marker_color='#e74c3c'),
            row=1, col=2
        )
        
        # Category (Pie)
        fig.add_trace(
            go.Pie(labels=cat_sales['Product_Category'], values=cat_sales['Revenue'], name="Category",
                   marker=dict(colors=colors)),
            row=2, col=1
        )
        
        # Top Products
        top_10 = df.groupby('Product_Name')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True).tail(10)
        fig.add_trace(
            go.Bar(x=top_10['Profit'], y=top_10['Product_Name'], orientation='h', name='Profit', marker_color='#9b59b6'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text=f"Interactive Sales Performance Dashboard (Total Revenue: ${total_revenue:,.2f})",
            height=800, 
            showlegend=True,
            template="plotly_dark",
            paper_bgcolor="#1e1e24",
            plot_bgcolor="#1e1e24"
        )
        
        fig.write_html("visualizations/interactive_sales_dashboard.html")
        print("[+] Saved interactive dashboard to visualizations/interactive_sales_dashboard.html")
        
    except ImportError:
        print("[*] Plotly not installed. Skipping interactive dashboard generation.")
        
    # Save key metrics to a summary file
    summary_data = {
        'Metric': ['Total Revenue', 'Total Cost', 'Total Profit', 'Total Units Sold', 'Average Order Value', 'Profit Margin (%)'],
        'Value': [total_revenue, total_cost, total_profit, total_units, avg_order_value, overall_margin]
    }
    pd.DataFrame(summary_data).to_csv("sales_performance_summary.csv", index=False)
    print("[+] Saved summary metrics to sales_performance_summary.csv")
    print("[+] Sales analysis pipeline completed successfully!")

if __name__ == "__main__":
    main()
