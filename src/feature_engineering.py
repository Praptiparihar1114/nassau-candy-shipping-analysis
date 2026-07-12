import pandas as pd
from config import FACTORY_COORDS, PRODUCT_TO_FACTORY


def add_factory_info(df):
    df = df.copy()
    df["Factory"] = df["Product Name"].map(PRODUCT_TO_FACTORY)

    unmapped = df["Factory"].isna()
    if unmapped.any():
        print(f"warning: {unmapped.sum()} rows with product not in PRODUCT_TO_FACTORY: "
              f"{df.loc[unmapped, 'Product Name'].unique()[:5]}")
        df = df[~unmapped]

    df["Factory Lat"] = df["Factory"].map(lambda f: FACTORY_COORDS[f][0])
    df["Factory Lon"] = df["Factory"].map(lambda f: FACTORY_COORDS[f][1])
    return df


def add_route_features(df):
    df = df.copy()
    df["Route (Region)"] = df["Factory"] + " -> " + df["Region"]
    df["Route (State)"] = df["Factory"] + " -> " + df["State/Province"]
    return df


def engineer_features(df):
    df = add_factory_info(df)
    df = add_route_features(df)
    return df


if __name__ == "__main__":
    df_leadtime = pd.read_csv("../data/orders_leadtime.csv")
    df_features = engineer_features(df_leadtime)
    df_features.to_csv("../data/orders_features.csv", index=False)
    print(f"final table: {df_features.shape}")
    print(df_features["Route (State)"].nunique(), "state routes")
    print(df_features["Route (Region)"].nunique(), "region routes")
