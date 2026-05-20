import csv
import random
from datetime import datetime, timedelta

def main():
    print("[*] Generating sales performance dataset...")
    
    # Categories, Products, and Unit Prices / Cost Prices
    catalog = {
        "Electronics": {
            "Smartphone": (600, 420),
            "Laptop": (1000, 750),
            "Tablet": (400, 290),
            "Headphones": (150, 95),
            "Smartwatch": (250, 180)
        },
        "Fashion": {
            "T-Shirt": (25, 10),
            "Jeans": (60, 25),
            "Jacket": (120, 60),
            "Sneakers": (80, 40),
            "Watch": (180, 100)
        },
        "Home & Kitchen": {
            "Coffee Maker": (90, 55),
            "Blender": (60, 38),
            "Air Fryer": (120, 78),
            "Vacuum Cleaner": (200, 130),
            "Microwave": (150, 95)
        },
        "Sports & Outdoors": {
            "Yoga Mat": (30, 12),
            "Dumbbells Set": (80, 50),
            "Treadmill": (800, 550),
            "Water Bottle": (20, 6),
            "Backpack": (50, 22)
        }
    }
    
    regions = {
        "North": ["New Delhi", "Mumbai", "Chandigarh"],
        "South": ["Bangalore", "Chennai", "Hyderabad"],
        "East": ["Kolkata", "Guwahati", "Bhubaneswar"],
        "West": ["Pune", "Ahmedabad", "Jaipur"]
    }
    
    customer_segments = ["Consumer", "Corporate", "Home Office"]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_delta = (end_date - start_date).days
    
    headers = [
        "Transaction_ID", "Date", "Customer_Segment", 
        "Region", "City", "Product_Category", "Product_Name", 
        "Units_Sold", "Unit_Price", "Cost_Price", "Discount_Pct", 
        "Revenue", "Cost", "Profit"
    ]
    
    records = []
    
    # Generate 5000 transactions over 2 years
    for i in range(1, 5001):
        tx_id = f"TX{i:05d}"
        
        # Select date
        days_offset = random.randint(0, date_delta)
        tx_date = start_date + timedelta(days=days_offset)
        # Introduce a seasonal sales trend (higher sales in November/December and regional preferences)
        month = tx_date.month
        
        # Decide category and product
        category = random.choices(list(catalog.keys()), weights=[0.35, 0.25, 0.20, 0.20])[0]
        product = random.choice(list(catalog[category].keys()))
        unit_price, cost_price = catalog[category][product]
        
        # Region and city
        region = random.choices(list(regions.keys()), weights=[0.35, 0.25, 0.20, 0.20])[0]
        city = random.choice(regions[region])
        
        # Units sold (more units for cheaper items)
        if unit_price > 500:
            units = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03])[0]
        elif unit_price > 100:
            units = random.randint(1, 4)
        else:
            units = random.randint(1, 10)
            
        # Boost sales in Q4 (Oct-Dec)
        if month in [10, 11, 12]:
            units = int(units * random.uniform(1.2, 1.5))
            units = max(1, units)
            
        segment = random.choices(customer_segments, weights=[0.5, 0.3, 0.2])[0]
        
        # Discount
        discount_pct = random.choices([0.0, 0.05, 0.1, 0.15, 0.2], weights=[0.55, 0.2, 0.15, 0.07, 0.03])[0]
        
        # Revenue, Cost, Profit calculations
        gross_revenue = units * unit_price
        discount_amount = gross_revenue * discount_pct
        revenue = round(gross_revenue - discount_amount, 2)
        cost = round(units * cost_price, 2)
        profit = round(revenue - cost, 2)
        
        records.append([
            tx_id, tx_date.strftime("%Y-%m-%d"), segment,
            region, city, category, product,
            units, unit_price, cost_price, discount_pct,
            revenue, cost, profit
        ])
        
    # Sort by date
    records.sort(key=lambda x: x[1])
    
    with open("sales_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} sales records in sales_data.csv.")

if __name__ == "__main__":
    main()
