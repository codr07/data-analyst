import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("[*] Starting Marketing Campaign Effectiveness Analysis...")
    db_name = "marketing.db"
    
    if not os.path.exists(db_name):
        print(f"[-] Database {db_name} not found! Run generate_data.py first.")
        return
        
    conn = sqlite3.connect(db_name)
    
    # Query 1: Campaign ROI and CAC Analysis
    query_roi = """
    SELECT 
        c.campaign_id,
        c.campaign_name,
        c.channel,
        c.budget,
        COUNT(conv.conversion_id) AS total_conversions,
        ROUND(SUM(conv.revenue), 2) AS total_revenue,
        ROUND(SUM(conv.revenue) - c.budget, 2) AS net_profit,
        ROUND((SUM(conv.revenue) / c.budget) * 100, 2) AS roi_pct,
        ROUND(c.budget / COUNT(conv.conversion_id), 2) AS cac
    FROM campaigns c
    LEFT JOIN conversions conv ON c.campaign_id = conv.campaign_id
    GROUP BY c.campaign_id
    ORDER BY roi_pct DESC
    """
    
    # Query 2: Acquisition Channel Performance
    query_channel = """
    SELECT 
        c.channel,
        SUM(c.budget) AS total_budget,
        COUNT(conv.conversion_id) AS total_conversions,
        ROUND(SUM(conv.revenue), 2) AS total_revenue,
        ROUND((SUM(conv.revenue) / SUM(c.budget)) * 100, 2) AS channel_roi_pct
    FROM campaigns c
    LEFT JOIN conversions conv ON c.campaign_id = conv.campaign_id
    GROUP BY c.channel
    ORDER BY channel_roi_pct DESC
    """
    
    # Load into Pandas
    df_roi = pd.read_sql_query(query_roi, conn)
    df_channel = pd.read_sql_query(query_channel, conn)
    
    conn.close()
    
    print("\n" + "="*80)
    print("                    CAMPAIGN ROI & CAC PERFORMANCE")
    print("="*80)
    print(df_roi.to_string(index=False))
    print("="*80)
    
    print("\n" + "="*80)
    print("                    CHANNEL PERFORMANCE SUMMARY")
    print("="*80)
    print(df_channel.to_string(index=False))
    print("="*80)
    
    # Save CSV reports
    df_roi.to_csv("campaign_roi_report.csv", index=False)
    df_channel.to_csv("channel_performance_report.csv", index=False)
    print("\n[+] Saved reports to campaign_roi_report.csv and channel_performance_report.csv")
    
    # Create visualizations
    os.makedirs("visualizations", exist_ok=True)
    
    # Plot 1: ROI by Campaign
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71' if x >= 100 else '#e74c3c' for x in df_roi['roi_pct']]
    plt.bar(df_roi['campaign_name'], df_roi['roi_pct'], color=colors, edgecolor='none', width=0.6)
    plt.axhline(100, color='#7f8c8d', linestyle='--', alpha=0.7, label='Break-Even Point (100% ROI)')
    plt.title('Return on Investment (ROI %) by Campaign', fontsize=14, fontweight='bold', color='#2c3e50')
    plt.ylabel('ROI (%)')
    plt.xticks(rotation=30)
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/campaign_roi.png", dpi=150)
    plt.close()
    
    # Plot 2: Budget vs Revenue Comparison
    plt.figure(figsize=(10, 6))
    x_indices = range(len(df_roi))
    width = 0.35
    plt.bar([x - width/2 for x in x_indices], df_roi['budget'], width, label='Budget', color='#3498db')
    plt.bar([x + width/2 for x in x_indices], df_roi['total_revenue'], width, label='Revenue', color='#2ecc71')
    plt.xticks(x_indices, df_roi['campaign_name'], rotation=30)
    plt.title('Campaign Budget vs Revenue Generated', fontsize=14, fontweight='bold', color='#2c3e50')
    plt.ylabel('Amount ($)')
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/budget_vs_revenue.png", dpi=150)
    plt.close()
    
    print("[+] Saved charts to visualizations/campaign_roi.png and visualizations/budget_vs_revenue.png")
    print("[+] Marketing Campaign analysis finished successfully!")

if __name__ == "__main__":
    main()
