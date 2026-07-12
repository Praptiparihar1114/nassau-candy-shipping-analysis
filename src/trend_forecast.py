import numpy as np
import pandas as pd


def monthly_trend(df):
    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)

    trend = df.groupby("Order Month").agg(
        Avg_Lead_Time=("Lead Time (days)", "mean"),
        Shipments=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
    ).reset_index().sort_values("Order Month")
    return trend


def forecast_next_month(trend, column="Avg_Lead_Time", periods=1):
    # simple linear fit, kept intentionally basic - a metric this
    # noisy doesn't need (or deserve) a fancier model
    x = np.arange(len(trend))
    y = trend[column].values
    coeffs = np.polyfit(x, y, deg=1)
    poly = np.poly1d(coeffs)

    future_x = np.arange(len(trend), len(trend) + periods)
    future_y = poly(future_x)

    last_period = pd.Period(trend["Order Month"].iloc[-1], freq="M")
    future_months = [str(last_period + i) for i in range(1, periods + 1)]

    return pd.DataFrame({"Order Month": future_months, f"Forecast_{column}": future_y})


if __name__ == "__main__":
    df = pd.read_csv("../data/orders_features.csv")
    trend = monthly_trend(df)
    print(trend)
    forecast = forecast_next_month(trend, "Avg_Lead_Time", periods=3)
    print(forecast)
    trend.to_csv("../outputs/monthly_trend.csv", index=False)
