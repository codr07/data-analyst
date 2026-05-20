import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    print("[*] Starting Customer Segmentation Analysis...")
    db_name = "customer_data.db"
    
    if not os.path.exists(db_name):
        print(f"[-] Database {db_name} not found! Please run generate_data.py first.")
        return
        
    # Connect to sqlite
    conn = sqlite3.connect(db_name)
    
    # Query to calculate Recency, Frequency, Monetary value
    # Reference date is '2026-05-20'
    query = """
    SELECT 
        c.customer_id,
        c.age,
        c.income,
        c.gender,
        JULIANDAY('2026-05-20') - JULIANDAY(MAX(p.purchase_date)) AS recency,
        COUNT(p.purchase_id) AS frequency,
        SUM(p.amount) AS monetary
    FROM customers c
    JOIN purchases p ON c.customer_id = p.customer_id
    GROUP BY c.customer_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"[+] Loaded {len(df)} customer records for analysis.")
    
    # Features for clustering
    features = ['recency', 'frequency', 'monetary']
    X = df[features]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply KMeans (K=4 based on generated profiles)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Analyze cluster profiles
    cluster_summary = df.groupby('cluster').agg({
        'customer_id': 'count',
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean',
        'age': 'mean',
        'income': 'mean'
    }).rename(columns={'customer_id': 'customer_count'})
    
    # Assign readable profile names based on characteristics
    # Cluster sorting by monetary value
    sorted_clusters = cluster_summary.sort_values(by='monetary').index.tolist()
    profile_mapping = {
        sorted_clusters[0]: "Dormant/Low-Value",
        sorted_clusters[1]: "Budget Shoppers",
        sorted_clusters[2]: "Regular Value Shoppers",
        sorted_clusters[3]: "VIP/Premium Shoppers"
    }
    df['segment'] = df['cluster'].map(profile_mapping)
    
    # Recalculate summary with segment names
    summary = df.groupby('segment').agg({
        'customer_id': 'count',
        'recency': ['mean', 'min', 'max'],
        'frequency': ['mean', 'min', 'max'],
        'monetary': ['mean', 'min', 'max'],
        'age': 'mean',
        'income': 'mean'
    })
    
    # Create visualizations folder
    os.makedirs("visualizations", exist_ok=True)
    
    # Save statistics report
    summary.to_csv("customer_segments_summary.csv")
    print("[+] Saved segment summary to customer_segments_summary.csv")
    
    # Visualization: 3D Scatter Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = {'VIP/Premium Shoppers': '#FFD700', 
              'Regular Value Shoppers': '#1f77b4', 
              'Budget Shoppers': '#2ca02c', 
              'Dormant/Low-Value': '#d62728'}
    
    for segment, group in df.groupby('segment'):
        ax.scatter(group['recency'], group['frequency'], group['monetary'], 
                   label=segment, c=colors[segment], s=40, alpha=0.7, edgecolors='w')
        
    ax.set_xlabel('Recency (Days since last purchase)')
    ax.set_ylabel('Frequency (Total purchases)')
    ax.set_zlabel('Monetary (Total Spent)')
    ax.set_title('Customer Segments (RFM Clustering)', fontsize=14, fontweight='bold')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig("visualizations/customer_rfm_clusters.png", dpi=150)
    plt.close()
    
    # Save another plot: Distribution of income vs spending per cluster
    plt.figure(figsize=(10, 6))
    for segment, group in df.groupby('segment'):
        plt.scatter(group['income'], group['monetary'], label=segment, c=colors[segment], alpha=0.6, edgecolors='none', s=50)
    plt.xlabel('Annual Income (USD)')
    plt.ylabel('Monetary (Total Spend)')
    plt.title('Income vs. Spending by Customer Segment', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("visualizations/income_vs_spending.png", dpi=150)
    plt.close()
    
    print("[+] Successfully generated visualizations in visualizations/ folder.")
    print("[+] Customer Segmentation Analysis finished successfully!")

if __name__ == "__main__":
    main()
