import numpy as np
import pandas as pd
from config import SIMULATED_LEAD_TIME_RANGES, RANDOM_SEED


def simulate_lead_time(df):
    df = df.copy()
    rng = np.random.default_rng(RANDOM_SEED)

    lead_times = np.empty(len(df), dtype=float)
    for mode, (lo, hi) in SIMULATED_LEAD_TIME_RANGES.items():
        mask = (df["Ship Mode"] == mode).to_numpy()
        n = mask.sum()
        if n:
            lead_times[mask] = rng.uniform(lo, hi, size=n)

    unmapped = ~df["Ship Mode"].isin(SIMULATED_LEAD_TIME_RANGES.keys())
    if unmapped.any():
        print(f"warning: {unmapped.sum()} rows have unmapped ship mode: "
              f"{df.loc[unmapped, 'Ship Mode'].unique()}")

    df["Lead Time (days)"] = np.round(lead_times, 2)
    return df


if __name__ == "__main__":
    df_clean = pd.read_csv("../data/orders_clean.csv")
    df_sim = simulate_lead_time(df_clean)
    print(df_sim.groupby("Ship Mode")["Lead Time (days)"].describe())
    df_sim.to_csv("../data/orders_leadtime.csv", index=False)
