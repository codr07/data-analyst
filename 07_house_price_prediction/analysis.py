import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("[*] Starting House Price Prediction Modeling...")
    csv_file = "housing_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} housing data points.")
    
    # Separate features and target
    features = ["Size_SqFt", "Bedrooms", "Bathrooms", "Location_Score", "Age_Years", "Garage_Spaces"]
    X = df[features]
    y = df["Price"]
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Ridge Regression
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train_scaled, y_train)
    ridge_preds = ridge.predict(X_test_scaled)
    
    # Train Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=150, random_state=42)
    rf.fit(X_train, y_train) # Random Forest doesn't strictly need scaling
    rf_preds = rf.predict(X_test)
    
    # Calculate performance metrics
    metrics = {
        'Model': ['Ridge Regression', 'Random Forest'],
        'MAE': [mean_absolute_error(y_test, ridge_preds), mean_absolute_error(y_test, rf_preds)],
        'RMSE': [root_mean_squared_error(y_test, ridge_preds), root_mean_squared_error(y_test, rf_preds)],
        'R2_Score': [r2_score(y_test, ridge_preds), r2_score(y_test, rf_preds)]
    }
    
    metrics_df = pd.DataFrame(metrics)
    print("\n" + "="*60)
    print("                    MODEL PERFORMANCE COMPARISON")
    print("="*60)
    print(metrics_df.to_string(index=False))
    print("="*60)
    
    # Save performance metrics
    metrics_df.to_csv("regression_model_comparison.csv", index=False)
    print("[+] Saved metrics report to regression_model_comparison.csv")
    
    # Create visualizations
    os.makedirs("visualizations", exist_ok=True)
    
    # Plot 1: Actual vs Predicted Prices (Random Forest)
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, rf_preds, alpha=0.6, color='#3498db', edgecolors='w', s=40)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Fit')
    plt.title('Actual vs. Predicted House Prices (Random Forest)', fontsize=12, fontweight='bold', color='#2c3e50')
    plt.xlabel('Actual Price ($)')
    plt.ylabel('Predicted Price ($)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/actual_vs_predicted.png", dpi=150)
    plt.close()
    
    # Plot 2: Feature Importance (Random Forest)
    importances = rf.feature_importances_
    feat_imp = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feat_imp, x='Importance', y='Feature', palette='viridis')
    plt.title('Feature Importances for Price Prediction (Random Forest)', fontsize=12, fontweight='bold', color='#2c3e50')
    plt.xlabel('Relative Importance')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("visualizations/feature_importances.png", dpi=150)
    plt.close()
    
    print("[+] Saved charts to visualizations/actual_vs_predicted.png and visualizations/feature_importances.png")
    print("[+] House Price Prediction modeling finished successfully!")

if __name__ == "__main__":
    main()
