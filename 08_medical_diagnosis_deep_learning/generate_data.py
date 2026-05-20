import csv
import math
import random

def main():
    print("[*] Generating patient diagnostic dataset...")
    
    headers = ["Patient_ID", "Age", "BMI", "Blood_Pressure", "Glucose_Level", "Cholesterol", "Insulin", "Diagnosis"]
    records = []
    
    # Sigmoid model:
    # z = -8.0 + 0.04*Age + 0.15*BMI + 0.02*Blood_Pressure + 0.05*Glucose_Level + 0.01*Cholesterol + 0.005*Insulin
    # P(Disease) = 1 / (1 + exp(-z))
    
    for i in range(1, 1001):
        patient_id = f"PT{i:04d}"
        age = random.randint(18, 80)
        bmi = round(random.uniform(17.0, 42.0), 1)
        bp = random.randint(60, 150)
        glucose = random.randint(70, 250)
        cholesterol = random.randint(120, 320)
        insulin = random.randint(15, 300)
        
        # Calculate log-odds z
        z = (-7.5 + 
             0.03 * age + 
             0.14 * bmi + 
             0.015 * bp + 
             0.04 * glucose + 
             0.008 * cholesterol + 
             0.003 * insulin)
             
        # Convert to probability
        prob = 1.0 / (1.0 + math.exp(-z))
        
        # Determine diagnosis (0 = Healthy, 1 = Diagnosed/High Risk)
        diagnosis = 1 if random.random() < prob else 0
        
        records.append([patient_id, age, bmi, bp, glucose, cholesterol, insulin, diagnosis])
        
    with open("patient_records.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} patient records in patient_records.csv.")

if __name__ == "__main__":
    main()
