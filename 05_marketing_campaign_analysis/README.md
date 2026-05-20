# 🎯 Marketing Campaign Effectiveness Analysis

This project analyzes the performance and financial returns of multi-channel marketing campaigns. Using a structured SQLite database containing tables for campaigns, customer signups, and transactional conversions, it executes advanced SQL queries to evaluate key performance metrics like Return on Investment (ROI), Customer Acquisition Cost (CAC), and channel performance.

## 🎯 Objectives
- Build an SQLite relational database mapping customers, campaigns, and purchasing events.
- Write relational SQL queries utilizing JOINs and aggregations to track business performance.
- Compute Campaign ROI (Return on Investment %) and CAC (Customer Acquisition Cost).
- Visualize campaign performance metrics for business reporting.

## 🛠️ Tech Stack
- **Database**: SQLite (relational engine)
- **Data Engineering**: Python, SQLite3, Pandas
- **Data Visualization**: Matplotlib

## 📊 Database Schema & SQL Metrics
The database `marketing.db` contains three tables:
1. `campaigns`: campaign metadata (`campaign_id`, `campaign_name`, `channel`, `budget`, `start_date`, `end_date`).
2. `users`: subscriber list (`user_id`, `acquisition_channel`, `signup_date`).
3. `conversions`: transactional actions linked to campaigns (`conversion_id`, `user_id`, `campaign_id`, `conversion_date`, `revenue`).

### SQL Calculations:
- **ROI (%)**:
  $$\text{ROI} = \left(\frac{\text{Total Revenue Generated}}{\text{Campaign Budget}}\right) \times 100$$
- **CAC**:
  $$\text{CAC} = \frac{\text{Campaign Budget}}{\text{Total Conversions Generated}}$$

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Build the SQLite database and populate it with historical records:
   ```bash
   python generate_data.py
   ```
3. Run the SQL analysis and visualization script:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `marketing.db`: Configured SQLite database.
- `campaign_roi_report.csv`: Table containing metrics (Revenue, Budget, ROI %, CAC, Net Profit) per campaign.
- `channel_performance_report.csv`: Performance summary aggregated by marketing channel (e.g. Email, Social Media, Search).
- `visualizations/campaign_roi.png`: Bar chart contrasting ROI % by campaign against the break-even baseline.
- `visualizations/budget_vs_revenue.png`: Double bar chart comparing budget allocated against revenue generated.
