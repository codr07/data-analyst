import sqlite3
import random
from datetime import datetime, timedelta

def main():
    print("[*] Generating customer segmentation data...")
    db_name = "customer_data.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        join_date TEXT,
        age INTEGER,
        gender TEXT,
        income INTEGER
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        purchase_date TEXT,
        amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)
    
    # Clear existing data to allow fresh generation
    cursor.execute("DELETE FROM purchases")
    cursor.execute("DELETE FROM customers")
    
    # Generate 500 customers with specific profiles (to make clustering distinct)
    genders = ["Male", "Female", "Non-binary"]
    customers = []
    
    # Profiles:
    # 1. Budget shoppers (young, lower income, frequent small purchases)
    # 2. Premium shoppers (middle age, high income, infrequent high value purchases)
    # 3. Regular value shoppers (any age, average income, regular average purchases)
    # 4. Dormant/Churned shoppers (joined long ago, haven't bought recently)
    
    base_date = datetime(2025, 1, 1)
    
    for cid in range(1, 501):
        profile = random.choices([1, 2, 3, 4], weights=[0.3, 0.2, 0.4, 0.1])[0]
        join_days_ago = random.randint(30, 365)
        join_date = (base_date - timedelta(days=join_days_ago)).strftime("%Y-%m-%d")
        
        if profile == 1:
            age = random.randint(18, 25)
            income = random.randint(20000, 40000)
        elif profile == 2:
            age = random.randint(35, 60)
            income = random.randint(90000, 150000)
        elif profile == 3:
            age = random.randint(22, 50)
            income = random.randint(45000, 85000)
        else:
            age = random.randint(25, 65)
            income = random.randint(30000, 100000)
            
        gender = random.choices(genders, weights=[0.48, 0.48, 0.04])[0]
        customers.append((cid, join_date, age, gender, income))
        
    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers)
    
    # Generate purchases
    purchases = []
    for cid, join_date, age, gender, income in customers:
        # Determine behavior based on profile
        # Recency is calculated relative to a reference date of "2026-05-20"
        ref_date = datetime(2026, 5, 20)
        join_dt = datetime.strptime(join_date, "%Y-%m-%d")
        total_days = (ref_date - join_dt).days
        
        # Determine profile implicitly again
        if age <= 25 and income <= 40000: # budget
            num_purchases = random.randint(8, 25)
            amount_range = (10.0, 45.0)
            recent_delta_max = 20
        elif age >= 35 and income >= 90000: # premium
            num_purchases = random.randint(2, 6)
            amount_range = (150.0, 500.0)
            recent_delta_max = 60
        elif join_dt < datetime(2025, 6, 1) and random.random() < 0.8: # dormant (simulate profile 4)
            num_purchases = random.randint(1, 3)
            amount_range = (15.0, 100.0)
            recent_delta_max = total_days
            # Force them to be inactive for at least 180 days
            total_days = max(180, total_days)
        else: # regular
            num_purchases = random.randint(4, 15)
            amount_range = (30.0, 120.0)
            recent_delta_max = 45
            
        for _ in range(num_purchases):
            days_ago = random.randint(1, min(total_days, recent_delta_max))
            p_date = (ref_date - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
            amount = round(random.uniform(*amount_range), 2)
            purchases.append((cid, p_date, amount))
            
    cursor.executemany("INSERT INTO purchases (customer_id, purchase_date, amount) VALUES (?, ?, ?)", purchases)
    
    conn.commit()
    conn.close()
    print(f"[+] Successfully generated {len(customers)} customers and {len(purchases)} purchases in customer_data.db.")

if __name__ == "__main__":
    main()
