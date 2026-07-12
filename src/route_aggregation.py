import pandas as pd
from config import DELAY_THRESHOLD_DAYS


def aggregate_routes(df, route_col="Route (State)"):
    grouped = df.groupby(route_col).agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time (days)", "mean"),
        Lead_Time_StdDev=("Lead Time (days)", "std"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
    ).reset_index()

    delay_rate = (
        df.assign(Is_Delayed=df["Lead Time (days)"] > DELAY_THRESHOLD_DAYS)
        .groupby(route_col)["Is_Delayed"]
        .mean()
        .rename("Delay_Frequency")
        .reset_index()
    )

    grouped = grouped.merge(delay_rate, on=route_col)
    grouped["Lead_Time_StdDev"] = grouped["Lead_Time_StdDev"].fillna(0)
    return grouped.sort_values("Avg_Lead_Time")


if __name__ == "__main__":
    df_features = pd.read_csv("../data/orders_features.csv")
    route_summary = aggregate_routes(df_features, route_col="Route (State)")
    route_summary.to_csv("../outputs/route_summary.csv", index=False)
