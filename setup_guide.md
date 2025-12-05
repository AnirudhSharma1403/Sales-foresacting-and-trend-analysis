# Setup Guide: Sales Forecasting with Time-Series Models

## Prerequisites
- PostgreSQL database (e.g., Neon.tech or ElephantSQL)
- Power BI Desktop / Service
- GitHub account

## Steps
1. Upload dataset to `data/monthly_sales.csv`.
2. Add PostgreSQL connection string to GitHub Secrets as `POSTGRES_URL`.
3. Run the script manually or wait for the GitHub Action schedule.
4. Connect Power BI to PostgreSQL table `sales_forecast`.
5. Publish the dashboard and embed it on Hostinger.
