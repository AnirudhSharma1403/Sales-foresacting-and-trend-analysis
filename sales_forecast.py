import os, pandas as pd, sqlalchemy
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

POSTGRES_URL = os.getenv("POSTGRES_URL")

df = pd.read_csv("data/monthly_sales.csv", parse_dates=["date"])
df = df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

df_prophet = df.rename(columns={"date": "ds", "sales": "y"})
model = Prophet()
model.fit(df_prophet)

future = model.make_future_dataframe(periods=6, freq="M")
forecast = model.predict(future)

forecast_df = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].merge(
    df_prophet, on="ds", how="left"
)

mask = forecast_df["y"].notnull()
mae = mean_absolute_error(forecast_df.loc[mask, "y"], forecast_df.loc[mask, "yhat"])
mape = mean_absolute_percentage_error(forecast_df.loc[mask, "y"], forecast_df.loc[mask, "yhat"])

forecast_df["mae"] = mae
forecast_df["mape"] = round(mape * 100, 2)

engine = sqlalchemy.create_engine(POSTGRES_URL)
forecast_df.to_sql("sales_forecast", con=engine, if_exists="replace", index=False)
print(f"✅ Forecast complete! MAE={mae:.2f}, MAPE={mape*100:.2f}%")
