import pandas as pd


def load_raw_data(path):
    df = pd.read_csv(path)
    print(f"loaded {len(df):,} rows, {df.shape[1]} cols")
    return df


def clean_data(df):
    df = df.copy()
    n_start = len(df)

    # dates come in as DD-MM-YYYY
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")

    bad_dates = df["Order Date"].isna() | df["Ship Date"].isna()
    print(f"unparsable dates: {bad_dates.sum()}")
    df = df[~bad_dates]

    # Row ID is unique per row so we dedupe on everything else - Order ID +
    # Product ID is NOT a safe key here, same product can appear twice in
    # one order as separate line items with different qty/sales
    before = len(df)
    dedupe_cols = [c for c in df.columns if c != "Row ID"]
    df = df.drop_duplicates(subset=dedupe_cols, keep="first")
    print(f"duplicate rows dropped: {before - len(df)}")

    # keeping this around for reference/appendix but it's not reliable,
    # see config.py note - real lead time comes from lead_time_simulation.py
    df["Raw_Lead_Time_Days (UNRELIABLE)"] = (df["Ship Date"] - df["Order Date"]).dt.days

    for col in ["City", "State/Province", "Region", "Country/Region"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    required = ["Ship Mode", "Product Name", "State/Province", "Region"]
    missing_required = df[required].isna().any(axis=1)
    print(f"missing required fields: {missing_required.sum()}")
    df = df[~missing_required]

    # sanity check: Sales should roughly equal Gross Profit + Cost
    expected_sales = df["Gross Profit"] + df["Cost"]
    mismatch = (df["Sales"] - expected_sales).abs() > 0.05
    print(f"sales/profit mismatch rows: {mismatch.sum()}")

    print(f"final: {len(df):,} / {n_start:,} rows retained ({len(df)/n_start:.1%})")
    return df


if __name__ == "__main__":
    df_raw = load_raw_data("../data/orders_raw.csv")
    df_clean = clean_data(df_raw)
    df_clean.to_csv("../data/orders_clean.csv", index=False)
