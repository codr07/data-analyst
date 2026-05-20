import csv
import random

def main():
    print("[*] Generating house price prediction dataset...")
    
    headers = ["House_ID", "Size_SqFt", "Bedrooms", "Bathrooms", "Location_Score", "Age_Years", "Garage_Spaces", "Price"]
    records = []
    
    # Mathematical pricing model:
    # Price = 50000 + 150*Size_SqFt + 15000*Bedrooms + 10000*Bathrooms + 25000*Location_Score - 1200*Age_Years + 8000*Garage_Spaces + Noise
    
    for i in range(1, 1001):
        house_id = f"HS{i:04d}"
        size = random.randint(800, 4500)
        
        # Bedrooms correlated with size
        if size < 1200:
            bedrooms = random.choices([1, 2], weights=[0.4, 0.6])[0]
        elif size < 2500:
            bedrooms = random.randint(2, 4)
        else:
            bedrooms = random.randint(4, 6)
            
        # Bathrooms correlated with bedrooms
        bathrooms = max(1, bedrooms - random.randint(0, 1))
        # Sometimes half baths
        if random.random() > 0.5:
            bathrooms += 0.5
            
        location = round(random.uniform(1.0, 10.0), 1)
        age = random.randint(0, 80)
        
        if size > 2000:
            garage = random.choices([1, 2, 3], weights=[0.2, 0.6, 0.2])[0]
        else:
            garage = random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
            
        noise = random.normalvariate(0, 15000.0)
        
        # Calculate price based on the linear model
        price = (50000 + 
                 165.0 * size + 
                 12000.0 * bedrooms + 
                 9500.0 * bathrooms + 
                 22000.0 * location - 
                 850.0 * age + 
                 7500.0 * garage + 
                 noise)
        
        price = max(60000, round(price, -2)) # Round to nearest 100
        records.append([house_id, size, bedrooms, bathrooms, location, age, garage, price])
        
    with open("housing_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} house records in housing_data.csv.")

if __name__ == "__main__":
    main()
