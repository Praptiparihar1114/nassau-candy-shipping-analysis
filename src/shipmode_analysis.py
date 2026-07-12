import pandas as pd


def ship_mode_summary(df):
    summary = df.groupby("Ship Mode").agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time (days)", "mean"),
        Lead_Time_StdDev=("Lead Time (days)", "std"),
        Avg_Sales=("Sales", "mean"),
        Avg_Gross_Profit=("Gross Profit", "mean"),
    ).reset_index().sort_values("Avg_Lead_Time")
    return summary


def ship_mode_by_route(df, route_col="Route (State)"):
    return df.pivot_table(
        index=route_col, columns="Ship Mode",
        values="Lead Time (days)", aggfunc="mean"
    ).round(1)
