# Nassau Candy Distributor — Shipping Route Efficiency Analysis

Route-level shipping analysis for Nassau Candy Distributor. Cleans order/shipment
data, maps products to their source factory, builds Factory -> State/Region
routes, scores them on speed + consistency, flags bottlenecks, compares ship
modes, and plots a lead-time trend with a short forecast. All wrapped in a
Streamlit dashboard.

## Structure

```
nassau_candy_project/
├── data/
│   └── orders_raw.csv          # source dataset
├── src/
│   ├── config.py                   # factory coords, product mapping, lead time ranges
│   ├── data_cleaning.py            # phase 1
│   ├── lead_time_simulation.py     # phase 1b
│   ├── feature_engineering.py      # phase 2
│   ├── route_aggregation.py        # phase 3
│   ├── efficiency_benchmarking.py  # phase 4
│   ├── geographic_analysis.py      # phase 5
│   ├── shipmode_analysis.py        # phase 6
│   ├── trend_forecast.py           # phase 8
│   └── run_pipeline.py             # runs everything above
├── dashboard/
│   └── app.py
├── outputs/                    # generated CSVs land here
├── requirements.txt
└── .gitignore
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
cd src
python run_pipeline.py

cd ../dashboard
streamlit run app.py
```

## A heads up on the data

The raw `Ship Date` column doesn't line up with `Order Date` — Same Day
shipping shows the same multi-year "lead time" as Standard Class, which
obviously isn't real. Lead Time used throughout this project is simulated
per Ship Mode (see `src/config.py` and `src/lead_time_simulation.py`),
not pulled directly from the raw dates. Flagged clearly in the dashboard too.

## Deploying

Push to GitHub, then deploy on share.streamlit.io pointing at
`dashboard/app.py`. Make sure `data/orders_raw.csv` and everything in
`outputs/` gets committed since the app reads from those paths.
