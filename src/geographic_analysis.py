import pandas as pd


def flag_bottlenecks(route_summary, volume_pct=0.75, leadtime_pct=0.75):
    # bottleneck = high volume AND slow, that's what actually matters
    # operationally vs just "slow but nobody uses this route anyway"
    df = route_summary.copy()
    vol_threshold = df["Total_Shipments"].quantile(volume_pct)
    lead_threshold = df["Avg_Lead_Time"].quantile(leadtime_pct)

    df["Is_Bottleneck"] = (
        (df["Total_Shipments"] >= vol_threshold) &
        (df["Avg_Lead_Time"] >= lead_threshold)
    )
    return df


def state_region_summary(df):
    by_state = df.groupby("State/Province").agg(
        Avg_Lead_Time=("Lead Time (days)", "mean"),
        Shipments=("Order ID", "count"),
    ).reset_index()

    by_region = df.groupby("Region").agg(
        Avg_Lead_Time=("Lead Time (days)", "mean"),
        Shipments=("Order ID", "count"),
    ).reset_index()

    return {"by_state": by_state, "by_region": by_region}
