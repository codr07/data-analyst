# 📦 Sales Demand Forecasting

This project implements a time-series forecasting model using machine learning to predict daily sales demand. It features advanced lag and rolling window feature engineering, historical time-series decomposition, and an autoregressive forecasting simulator to project sales 90 days into the future.

## 🎯 Objectives
- Conduct time-series decomposition (isolating trend, seasonality, and residuals).
- Structure lag features ($t-1$, $t-7$, $t-14$, $t-30$) and rolling window aggregates.
- Train a Random Forest regressor to learn non-linear patterns (e.g., weekly fluctuations, end-of-year peaks).
- Generate and evaluate out-of-sample forecasts using standard metrics (MAE, RMSE, MAPE).
- Build a multi-step forecasting loop to project future demand.

## 🛠️ Tech Stack
- **Data Engineering**: Python, Pandas, Numpy
- **Forecasting & Modeling**: Scikit-learn (RandomForestRegressor), Statsmodels (seasonal_decompose)
- **Data Visualization**: Matplotlib

## ⚙️ Time Series Modeling Pipeline
1. **Feature Engineering**:
   - **Calendar attributes**: Day of week, day of year, week of year, month, quarter.
   - **Lag Features**: Historical sales values to capture short-term dependencies.
   - **Rolling aggregates**: 7-day and 30-day moving averages and moving standard deviations.
2. **Train-Test Partitioning**: Historical sales are split sequentially; the final 90 days are reserved for testing model accuracy.
3. **Model Fitting**: Random Forest regressor is fitted on training records.
4. **Iterative Autoregressive Forecasting**: Since future features depend on future sales, we run a simulated projection loop:
   - Predict $t+1$.
   - Insert predicted value back into history.
   - Recompute lags and rolling metrics.
   - Predict $t+2$ using the simulated features.
   - Repeat for 90 days.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic daily demand data:
   ```bash
   python generate_data.py
   ```
3. Run the modeling, evaluation, and future forecasting pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `daily_sales.csv`: 3 years of daily sales records with trend, seasonality, holidays, and noise.
- `forecast_evaluation_metrics.csv`: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE) calculated on the 90-day test set.
- `future_90day_forecast.csv`: Projections for 90 days following the end of the historical dataset.
- `visualizations/time_series_decomposition.png`: 4-panel additive decomposition chart (Trend, Seasonal, Residual, Observed).
- `visualizations/demand_forecast.png`: Chart showing historical data, test predictions, and future forecasts.
