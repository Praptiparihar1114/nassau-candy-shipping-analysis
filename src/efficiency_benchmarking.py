import pandas as pd


def compute_efficiency_score(route_summary):
    df = route_summary.copy()

    def normalize_inverse(series):
        rng = series.max() - series.min()
        if rng == 0:
            return pd.Series(100, index=series.index)
        return 100 * (1 - (series - series.min()) / rng)

    speed_score = normalize_inverse(df["Avg_Lead_Time"])
    consistency_score = normalize_inverse(df["Lead_Time_StdDev"])

    # 70% speed, 30% consistency - a fast but wildly inconsistent route
    # shouldn't outrank a moderately fast, reliable one
    df["Route_Efficiency_Score"] = (0.7 * speed_score + 0.3 * consistency_score).round(1)
    return df.sort_values("Route_Efficiency_Score", ascending=False)


def top_bottom_routes(scored_routes, route_col, n=10):
    ranked = scored_routes.sort_values("Route_Efficiency_Score", ascending=False)
    return ranked.head(n), ranked.tail(n).sort_values("Route_Efficiency_Score")


if __name__ == "__main__":
    route_summary = pd.read_csv("../outputs/route_summary.csv")
    scored = compute_efficiency_score(route_summary)
    top10, bottom10 = top_bottom_routes(scored, route_col="Route (State)")
    print(top10)
    print(bottom10)
