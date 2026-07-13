import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
import pandas as pd
import plotly.express as px

from route_aggregation import aggregate_routes
from efficiency_benchmarking import compute_efficiency_score, top_bottom_routes
from geographic_analysis import flag_bottlenecks, state_region_summary
from shipmode_analysis import ship_mode_summary
from trend_forecast import monthly_trend, forecast_next_month

st.set_page_config(page_title="Nassau Candy — Shipping Route Efficiency", layout="wide")

# plotly's US map wants 2-letter codes, not full state names
US_STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}


@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "orders_features.csv")
    return pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])


df = load_data()

st.title("Factory-to-Customer Shipping Route Efficiency")
st.caption("Nassau Candy Distributor — Logistics Analytics")

with st.expander("Note on Lead Time"):
    st.write(
        "The raw Ship Date column in the source file didn't line up with Order Date "
        "(Same Day shipping showed the same multi-year gap as Standard Class, which "
        "isn't physically possible). Lead Time here is simulated per Ship Mode using "
        "realistic ranges instead — see src/config.py."
    )

st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Order Date range",
    value=(df["Order Date"].min(), df["Order Date"].max()),
)
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
states = st.sidebar.multiselect("State/Province", sorted(df["State/Province"].unique()))
ship_modes = st.sidebar.multiselect("Ship Mode", sorted(df["Ship Mode"].unique()))
lead_time_max = st.sidebar.slider(
    "Max lead time (days)", 0.0, float(df["Lead Time (days)"].max()), float(df["Lead Time (days)"].max())
)

filtered = df.copy()
if len(date_range) == 2:
    filtered = filtered[
        (filtered["Order Date"] >= pd.Timestamp(date_range[0])) &
        (filtered["Order Date"] <= pd.Timestamp(date_range[1]))
    ]
if regions:
    filtered = filtered[filtered["Region"].isin(regions)]
if states:
    filtered = filtered[filtered["State/Province"].isin(states)]
if ship_modes:
    filtered = filtered[filtered["Ship Mode"].isin(ship_modes)]
filtered = filtered[filtered["Lead Time (days)"] <= lead_time_max]

if filtered.empty:
    st.warning("No data matches the current filters.")
    st.stop()

st.header("Route Efficiency Overview")
route_summary = aggregate_routes(filtered, route_col="Route (State)")
scored = compute_efficiency_score(route_summary)
top10, bottom10 = top_bottom_routes(scored, route_col="Route (State)", n=min(10, len(scored)))

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Top {len(top10)} Most Efficient Routes")
    display_df = top10[["Route (State)", "Avg_Lead_Time", "Total_Shipments", "Route_Efficiency_Score"]].fillna(0)
st.dataframe(display_df)
with col2:
    st.subheader(f"Bottom {len(bottom10)} Least Efficient Routes")
    st.dataframe(bottom10[["Route (State)", "Avg_Lead_Time", "Total_Shipments", "Route_Efficiency_Score"]].fillna(0))

st.download_button(
    "Download route summary (CSV)",
    data=scored.to_csv(index=False).encode("utf-8"),
    file_name="route_efficiency_summary.csv",
    mime="text/csv",
)

st.header("Geographic Shipping Map")
geo = state_region_summary(filtered)
us_geo = geo["by_state"].copy()
us_geo["Code"] = us_geo["State/Province"].map(US_STATE_ABBR)
us_geo = us_geo.dropna(subset=["Code"])

if us_geo.empty:
    st.info("No US states in the current filter selection.")
else:
    fig_map = px.choropleth(
        us_geo, locations="Code", locationmode="USA-states",
        color="Avg_Lead_Time", scope="usa", color_continuous_scale="RdYlGn_r",
        hover_name="State/Province",
        title="Average Lead Time by State"
    )
    st.plotly_chart(fig_map, use_container_width=True)

canada_states = set(geo["by_state"]["State/Province"]) - set(US_STATE_ABBR.keys())
if canada_states:
    st.caption(f"Canadian provinces in data (not on map above): {', '.join(sorted(canada_states))}")
    st.dataframe(geo["by_state"][geo["by_state"]["State/Province"].isin(canada_states)].fillna(0))
bottlenecks = flag_bottlenecks(route_summary)
st.subheader("Flagged Bottleneck Routes")
flagged = bottlenecks[bottlenecks["Is_Bottleneck"]]
if flagged.empty:
    st.info("No routes crossed the volume + lead-time thresholds for this filter.")
else:
   st.dataframe(flagged.fillna(0))

st.header("Ship Mode Comparison")
sm_summary = ship_mode_summary(filtered)
fig_sm = px.bar(sm_summary, x="Ship Mode", y="Avg_Lead_Time", title="Avg Lead Time by Ship Mode")
st.plotly_chart(fig_sm, use_container_width=True)
st.dataframe(sm_summary.fillna(0))

st.header("Trend & Forecast")
trend = monthly_trend(filtered)
if len(trend) >= 2:
    forecast = forecast_next_month(trend, "Avg_Lead_Time", periods=3)
    trend_plot = pd.concat([
        trend[["Order Month", "Avg_Lead_Time"]].assign(Type="Actual"),
        forecast.rename(columns={"Forecast_Avg_Lead_Time": "Avg_Lead_Time"}).assign(Type="Forecast"),
    ])
    fig_trend = px.line(
        trend_plot, x="Order Month", y="Avg_Lead_Time", color="Type", markers=True,
        title="Monthly Avg Lead Time — Actual vs Forecast"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Not enough months in this filter selection to plot a trend.")

st.header("Route Drill-Down")
selected_route = st.selectbox("Choose a route", sorted(filtered["Route (State)"].unique()))
route_orders = filtered[filtered["Route (State)"] == selected_route]
st.write(f"{len(route_orders)} orders on this route")
fig_timeline = px.scatter(
    route_orders, x="Order Date", y="Lead Time (days)",
    title=f"Order-level lead time: {selected_route}"
)
st.plotly_chart(fig_timeline, use_container_width=True)
