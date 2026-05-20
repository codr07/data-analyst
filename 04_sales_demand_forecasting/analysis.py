import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def create_features(df, label=None):
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week.astype(int)
    
    # Lag features
    for lag in [1, 7, 14, 30]:
        df[f'lag_{lag}'] = df['Sales_Demand'].shift(lag)
        
    # Rolling features
    df['rolling_mean_7'] = df['Sales_Demand'].shift(1).rolling(window=7).mean()
    df['rolling_mean_30'] = df['Sales_Demand'].shift(1).rolling(window=30).mean()
    df['rolling_std_7'] = df['Sales_Demand'].shift(1).rolling(window=7).std()
    
    X = df.drop(['Sales_Demand'], axis=1)
    if label:
        y = df[label]
        return X, y
    return X

def main():
    print("[*] Starting Sales Demand Forecasting...")
    csv_file = "daily_sales.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
    df = df.sort_index()
    print(f"[+] Loaded {len(df)} daily sales data points.")
    
    # Check for statsmodels for decomposition, run if available
    try:
        from statsmodels.tsa.seasonal import seasonal_decompose
        print("[*] statsmodels detected. Performing seasonal decomposition...")
        result = seasonal_decompose(df['Sales_Demand'], model='additive', period=365)
        
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        result.observed.plot(ax=axes[0], color='#34495e')
        axes[0].set_ylabel('Observed')
        result.trend.plot(ax=axes[1], color='#3498db')
        axes[1].set_ylabel('Trend')
        result.seasonal.plot(ax=axes[2], color='#2ecc71')
        axes[2].set_ylabel('Seasonal')
        result.resid.plot(ax=axes[3], style='.', color='#e74c3c')
        axes[3].set_ylabel('Residual')
        
        plt.suptitle('Time Series Decomposition (Additive)', fontsize=14, fontweight='bold')
        os.makedirs("visualizations", exist_ok=True)
        plt.tight_layout()
        plt.savefig("visualizations/time_series_decomposition.png", dpi=150)
        plt.close()
        print("[+] Saved seasonal decomposition to visualizations/time_series_decomposition.png")
    except Exception as e:
        print(f"[*] statsmodels decomposition skipped or failed: {e}")
        
    # Feature engineering for ML Model
    X, y = create_features(df, label='Sales_Demand')
    
    # Drop rows with NaN due to lagging/rolling operations
    valid_idx = X.dropna().index
    X_clean = X.loc[valid_idx]
    y_clean = y.loc[valid_idx]
    
    # Train-test split (train on history, test on last 90 days)
    split_date = y_clean.index[-90]
    X_train = X_clean.loc[X_clean.index < split_date]
    y_train = y_clean.loc[y_clean.index < split_date]
    X_test = X_clean.loc[X_clean.index >= split_date]
    y_test = y_clean.loc[y_clean.index >= split_date]
    
    print(f"[+] Training data size: {len(X_train)} rows. Test data size: {len(X_test)} rows.")
    
    # Fit Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    mape = np.mean(np.abs((y_test - preds) / y_test)) * 100
    
    print("\n" + "="*30)
    print("      MODEL PERFORMANCE METRICS")
    print("="*30)
    print(f"Mean Absolute Error (MAE): {mae:.2f} units")
    print(f"Root Mean Sq. Error (RMSE): {rmse:.2f} units")
    print(f"Mean Absolute % Error (MAPE): {mape:.2f}%")
    print("="*30)
    
    # Save validation metrics
    metrics_df = pd.DataFrame({
        'Metric': ['MAE', 'RMSE', 'MAPE (%)'],
        'Value': [mae, rmse, mape]
    })
    metrics_df.to_csv("forecast_evaluation_metrics.csv", index=False)
    
    # Forecast 90 Days into the future (iterative autoregressive forecast)
    print("[*] Generating 90-day future demand forecast...")
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=90, freq='D')
    
    # Copy dataframe for simulation
    sim_df = df.copy()
    
    for date in future_dates:
        # Create single row for prediction
        temp_df = pd.DataFrame(index=[date])
        # Add to sim_df with placeholder sales
        temp_df['Sales_Demand'] = np.nan
        sim_df = pd.concat([sim_df, temp_df])
        
        # Re-engineer features for the specific date
        X_sim, _ = create_features(sim_df, label='Sales_Demand')
        X_row = X_sim.loc[[date]]
        
        # Predict
        pred_val = model.predict(X_row)[0]
        # Store predicted value back into sim_df to serve as lag features for subsequent days
        sim_df.loc[date, 'Sales_Demand'] = pred_val
        
    future_forecast = sim_df.loc[future_dates, 'Sales_Demand']
    
    # Save future predictions
    future_forecast.to_csv("future_90day_forecast.csv")
    print("[+] Saved 90-day forecast to future_90day_forecast.csv")
    
    # Plot forecast
    plt.figure(figsize=(14, 7))
    plt.plot(df.index[-365:], df['Sales_Demand'].iloc[-365:], label='Historical Sales (Last 1 Year)', color='#34495e', linewidth=1.5)
    plt.plot(y_test.index, preds, label='Test Predictions (90 Days)', color='#e67e22', linestyle='--', linewidth=2)
    plt.plot(future_forecast.index, future_forecast.values, label='Future Forecast (90 Days)', color='#2ecc71', linewidth=2.5)
    
    plt.title('Sales Demand Forecasting (Random Forest Time Series Model)', fontsize=14, fontweight='bold', color='#2c3e50')
    plt.xlabel('Date')
    plt.ylabel('Sales Units')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    os.makedirs("visualizations", exist_ok=True)
    plt.tight_layout()
    plt.savefig("visualizations/demand_forecast.png", dpi=150)
    plt.close()
    
    print("[+] Saved forecast plot to visualizations/demand_forecast.png")
    print("[+] Sales Demand Forecasting completed successfully!")

if __name__ == "__main__":
    main()
