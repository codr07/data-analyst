# 🏡 House Price Prediction

This project builds a regression pipeline to estimate real estate property valuations. Using a dataset containing structural characteristics (Size, Bedrooms, Bathrooms, Garage size), age, and environmental ratings (Location grade), it scales input dimensions and trains regression estimators (Ridge and Random Forest) to predict market sale prices.

## 🎯 Objectives
- Build a supervised regression dataset with structural, age, and location features.
- Build a feature scaling preprocessing pipeline using Z-score standardization.
- Train and compare:
  - **Ridge Regression** (regularized linear model).
  - **Random Forest Regressor** (tree-based ensemble model).
- Evaluate performance metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared ($R^2$).
- Identify and visualize feature importances to determine key price drivers.

## 🛠️ Tech Stack
- **Data Engineering**: Python, Pandas, Numpy
- **Machine Learning**: Scikit-learn (Ridge, RandomForestRegressor, StandardScaler, train_test_split)
- **Data Visualization**: Matplotlib, Seaborn

## ⚙️ Regression Evaluation Metrics
- **Mean Absolute Error (MAE)**:
  $$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
- **Root Mean Squared Error (RMSE)**:
  $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$
- **Coefficient of Determination ($R^2$ Score)**:
  $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic housing features and prices:
   ```bash
   python generate_data.py
   ```
3. Run the regression modeling and feature analysis pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `housing_data.csv`: Clean tabular dataset representing 1,000 properties.
- `regression_model_comparison.csv`: Comparative performance metrics.
- `visualizations/actual_vs_predicted.png`: Scatter plot showcasing predicted values vs actual targets, mapped against a break-even diagonal.
- `visualizations/feature_importances.png`: Horizontal bar chart demonstrating the weight assigned to each physical attribute by the Random Forest model.
