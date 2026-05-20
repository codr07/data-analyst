import sqlite3
import random
import numpy as np
from datetime import datetime, timedelta

def main():
    print("[*] Generating marketing campaign database...")
    db_name = "marketing.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        campaign_id INTEGER PRIMARY KEY,
        campaign_name TEXT,
        channel TEXT,
        budget REAL,
        start_date TEXT,
        end_date TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        acquisition_channel TEXT,
        signup_date TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversions (
        conversion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        campaign_id INTEGER,
        conversion_date TEXT,
        revenue REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
    )
    """)
    
    # Clear existing data
    cursor.execute("DELETE FROM conversions")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM campaigns")
    
    # Define campaigns
    channels = ["Social Media", "Search Engine", "Email Marketing", "Influencer Blog"]
    campaigns = []
    
    # Generate 10 campaigns in 2025
    base_date = datetime(2025, 1, 1)
    
    for i in range(1, 11):
        name = f"Campaign_{i:02d}"
        channel = channels[i % 4]
        budget = round(random.uniform(2000.0, 15000.0), 2)
        start_days = (i - 1) * 30 + random.randint(1, 10)
        start_dt = base_date + timedelta(days=start_days)
        end_dt = start_dt + timedelta(days=random.randint(15, 45))
        
        campaigns.append((
            i, name, channel, budget, 
            start_dt.strftime("%Y-%m-%d"), 
            end_dt.strftime("%Y-%m-%d")
        ))
        
    cursor.executemany("INSERT INTO campaigns VALUES (?, ?, ?, ?, ?, ?)", campaigns)
    
    # Generate users and signups
    users = []
    total_users = 2500
    for uid in range(1, total_users + 1):
        channel = random.choices(channels, weights=[0.4, 0.3, 0.2, 0.1])[0]
        signup_days = random.randint(1, 350)
        signup_date = (base_date + timedelta(days=signup_days)).strftime("%Y-%m-%d")
        users.append((uid, channel, signup_date))
        
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
    
    # Generate conversions
    # A user can convert if they signed up after/during campaign
    conversions = []
    
    for camp_id, name, channel, budget, start, end in campaigns:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        
        # Filter users who joined in campaign period and have same channel (or random)
        eligible_users = [u[0] for u in users if start_dt <= datetime.strptime(u[2], "%Y-%m-%d") <= end_dt]
        
        if not eligible_users:
            continue
            
        # Determine conversion rate based on budget and channel efficiency
        # Social Media is decent, Email is highest ROI, Influencer is expensive/low conversion, Search is steady
        efficiency = {"Social Media": 0.15, "Search Engine": 0.12, "Email Marketing": 0.25, "Influencer Blog": 0.08}
        conv_rate = efficiency[channel] * (budget / 10000.0 + 0.5)
        conv_rate = min(0.4, max(0.02, conv_rate))
        
        num_conversions = int(len(eligible_users) * conv_rate)
        conv_users = random.sample(eligible_users, min(num_conversions, len(eligible_users)))
        
        for user_id in conv_users:
            # Conversion date between user signup and end of campaign
            u_signup = [u[2] for u in users if u[0] == user_id][0]
            u_signup_dt = datetime.strptime(u_signup, "%Y-%m-%d")
            
            c_start = max(start_dt, u_signup_dt)
            days_diff = (end_dt - c_start).days
            
            if days_diff <= 0:
                conv_date = c_start.strftime("%Y-%m-%d")
            else:
                conv_date = (c_start + timedelta(days=random.randint(0, days_diff))).strftime("%Y-%m-%d")
                
            revenue = round(np.random.exponential(scale=120.0) + 15.0, 2) # Exponential purchase amount
            conversions.append((user_id, camp_id, conv_date, revenue))
            
    cursor.executemany("INSERT INTO conversions (user_id, campaign_id, conversion_date, revenue) VALUES (?, ?, ?, ?)", conversions)
    
    conn.commit()
    conn.close()
    print(f"[+] Successfully generated {len(campaigns)} campaigns, {len(users)} users, and {len(conversions)} conversions in marketing.db.")

if __name__ == "__main__":
    main()
