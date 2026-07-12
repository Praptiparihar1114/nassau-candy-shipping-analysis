import pandas as pd
from data_cleaning import load_raw_data, clean_data
from lead_time_simulation import simulate_lead_time
from feature_engineering import engineer_features
from route_aggregation import aggregate_routes
from efficiency_benchmarking import compute_efficiency_score
from geographic_analysis import flag_bottlenecks
from trend_forecast import monthly_trend

RAW_PATH = "../data/orders_raw.csv"
FEATURES_PATH = "../data/orders_features.csv"


def main():
    print("== phase 1: cleaning ==")
    df = clean_data(load_raw_data(RAW_PATH))

    print("== phase 1b: lead time sim ==")
    df = simulate_lead_time(df)

    print("== phase 2: feature engineering ==")
    df = engineer_features(df)
    df.to_csv(FEATURES_PATH, index=False)
    print(f"saved -> {FEATURES_PATH} ({df.shape[0]} rows)")

    print("== phase 3-4: route aggregation + scoring ==")
    for level, col in [("state", "Route (State)"), ("region", "Route (Region)")]:
        route_summary = aggregate_routes(df, route_col=col)
        scored = compute_efficiency_score(route_summary)
        out_path = f"../outputs/route_summary_{level}.csv"
        scored.to_csv(out_path, index=False)
        print(f"{level}: {len(scored)} routes -> {out_path}")

    print("== phase 5: bottleneck flagging ==")
    route_summary_state = aggregate_routes(df, route_col="Route (State)")
    bottlenecks = flag_bottlenecks(route_summary_state)
    print(f"flagged: {bottlenecks['Is_Bottleneck'].sum()}")
    bottlenecks.to_csv("../outputs/bottleneck_routes.csv", index=False)

    print("== phase 8: trend ==")
    trend = monthly_trend(df)
    trend.to_csv("../outputs/monthly_trend.csv", index=False)
    print(f"saved {len(trend)} months")

    print("\ndone. run: streamlit run ../dashboard/app.py")


if __name__ == "__main__":
    main()
