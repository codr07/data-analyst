import csv
import math
import random
from datetime import datetime, timedelta

def main():
    print("[*] Generating daily sales demand dataset...")
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    delta_days = (end_date - start_date).days + 1
    
    records = []
    
    # Mathematical generation parameters:
    # y = base + trend*t + weekly_seasonality + annual_seasonality + noise
    base_sales = 300.0
    trend = 0.15 # Daily increase
    
    for t in range(delta_days):
        current_date = start_date + timedelta(days=t)
        
        # 1. Trend component
        y_trend = base_sales + (trend * t)
        
        # 2. Weekly seasonality (0 = Monday, ..., 6 = Sunday)
        day_of_week = current_date.weekday()
        if day_of_week in [4, 5]: # Friday, Saturday (peak)
            y_weekly = 75.0 + random.uniform(-10.0, 10.0)
        elif day_of_week == 6: # Sunday
            y_weekly = 40.0 + random.uniform(-5.0, 5.0)
        else: # Mon-Thu
            y_weekly = random.uniform(-15.0, 15.0)
            
        # 3. Annual seasonality (sinusoidal + holiday spikes)
        # Convert day of year to radians
        day_of_year = current_date.timetuple().tm_yday
        # Peak in summer (July, around day 190-210) and winter (December, around day 340-360)
        annual_angle = (day_of_year / 365.0) * 2.0 * math.pi
        y_annual = 50.0 * math.sin(annual_angle) + 40.0 * math.cos(annual_angle * 2.0)
        
        # Q4 Holiday spike (Nov 15 - Dec 31)
        if current_date.month == 12:
            y_annual += random.uniform(80.0, 150.0)
        elif current_date.month == 11 and current_date.day >= 15:
            y_annual += random.uniform(40.0, 90.0)
            
        # 4. Random noise (normally distributed representation)
        y_noise = random.normalvariate(0, 20.0)
        
        # Combine
        total_demand = y_trend + y_weekly + y_annual + y_noise
        total_demand = max(10, int(total_demand)) # Ensure no negative sales
        
        records.append([current_date.strftime("%Y-%m-%d"), total_demand])
        
    with open("daily_sales.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Sales_Demand"])
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} daily sales records in daily_sales.csv.")

if __name__ == "__main__":
    main()
