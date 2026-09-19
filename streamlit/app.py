import pandas as pd
import streamlit as st

from sqlalchemy import create_engine


# -------------------------
# Database
# -------------------------

DATABASE_URL = (
    "postgresql+psycopg2://myuser:Password123%21@localhost:5432/mydb"
)

engine = create_engine(DATABASE_URL)


def load_weather_data():
    query = """
        SELECT
            c.name AS city,
            c.latitude,
            c.longitude,
            w.forecast_date,
            w.temperature_max,
            w.temperature_min,
            w.precipitation,
            w.precipitation_probability,
            w.wind_speed_max,
            w.wind_gust_max,
            w.risk_score,
            w.risk_level
        FROM weather_forecasts w
        JOIN cities c ON c.id = w.city_id
        ORDER BY w.forecast_date;
    """

    return pd.read_sql(query, engine)


# -------------------------
# Page configuration
# -------------------------

st.set_page_config(
    page_title="Weather Risk Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Risk Dashboard")

st.write(
    "Weather forecasts and delivery risk monitoring across Morocco."
)


# -------------------------
# Load data
# -------------------------

df = load_weather_data()

df["forecast_date"] = pd.to_datetime(
    df["forecast_date"]
)


# -------------------------
# Sidebar filters
# -------------------------

st.sidebar.header("Filters")


cities = [
    "All"
] + sorted(
    df["city"]
    .dropna()
    .unique()
    .tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    cities
)


risk_levels = [
    "All"
] + sorted(
    df["risk_level"]
    .dropna()
    .unique()
    .tolist()
)

selected_risk = st.sidebar.selectbox(
    "Risk Level",
    risk_levels
)


start_date = st.sidebar.date_input(
    "Start Date",
    df["forecast_date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["forecast_date"].max().date()
)


# -------------------------
# Apply filters
# -------------------------

filtered_df = df[
    (df["forecast_date"].dt.date >= start_date)
    & (df["forecast_date"].dt.date <= end_date)
].copy()


if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["city"] == selected_city
    ]


if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]


if filtered_df.empty:
    st.warning(
        "No weather data found for the selected filters."
    )

    st.stop()


# -------------------------
# Prepare chart data
# -------------------------

if selected_city == "All":

    chart_df = (
        filtered_df
        .groupby(
            "forecast_date",
            as_index=False
        )
        .agg({
            "temperature_max": "mean",
            "temperature_min": "mean",
            "risk_score": "mean",
            "wind_gust_max": "max",
            "precipitation": "mean",
            "precipitation_probability": "mean"
        })
    )

else:

    chart_df = filtered_df.sort_values(
        "forecast_date"
    )


chart_dates = (
    chart_df["forecast_date"]
    .dt.strftime("%d %b")
    .tolist()
)


# -------------------------
# KPIs
# -------------------------

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Maximum Temperature",
    f"{filtered_df['temperature_max'].max():.1f} °C"
)


col2.metric(
    "Maximum Wind Gust",
    f"{filtered_df['wind_gust_max'].max():.1f} km/h"
)


col3.metric(
    "Average Risk",
    f"{filtered_df['risk_score'].mean():.1f}"
)


col4.metric(
    "Maximum Risk",
    f"{filtered_df['risk_score'].max():.1f}"
)


st.divider()


# -------------------------
# Map
# -------------------------

st.subheader("🗺️ Weather Locations")


map_dates = sorted(
    filtered_df[
        "forecast_date"
    ]
    .dt.date
    .unique()
)


selected_map_date = st.selectbox(
    "Map Date",
    map_dates
)


map_df = df[
    df["forecast_date"].dt.date
    == selected_map_date
][
    [
        "latitude",
        "longitude"
    ]
]


st.map(
    map_df,
    latitude="latitude",
    longitude="longitude",
    zoom=4
)


st.divider()


# -------------------------
# Risk Score
# -------------------------

st.subheader("⚠️ Risk Score Over Time")


risk_options = {

    "tooltip": {
        "trigger": "axis"
    },

    "xAxis": {
        "type": "category",
        "data": chart_dates
    },

    "yAxis": {
        "type": "value",
        "name": "Risk Score"
    },

    "series": [
        {
            "name": "Risk Score",

            "type": "line",

            "smooth": True,

            "data": (
                chart_df["risk_score"]
                .round(1)
                .tolist()
            ),

            "symbol": "circle",

            "symbolSize": 8,

            "lineStyle": {
                "width": 4
            },

            "areaStyle": {
                "opacity": 0.2
            }
        }
    ]
}


st.echarts_chart(
    risk_options,
    height=380,
    width="stretch"
)


# -------------------------
# Temperature
# -------------------------

st.subheader("🌡️ Temperature Forecast")


temperature_options = {

    "tooltip": {
        "trigger": "axis"
    },

    "legend": {
        "data": [
            "Maximum Temperature",
            "Minimum Temperature"
        ]
    },

    "xAxis": {
        "type": "category",
        "data": chart_dates
    },

    "yAxis": {
        "type": "value",
        "name": "°C"
    },

    "series": [
        {
            "name": "Maximum Temperature",

            "type": "line",

            "smooth": True,

            "data": (
                chart_df["temperature_max"]
                .round(1)
                .tolist()
            ),

            "symbol": "circle",

            "symbolSize": 8,

            "lineStyle": {
                "width": 4
            }
        },

        {
            "name": "Minimum Temperature",

            "type": "line",

            "smooth": True,

            "data": (
                chart_df["temperature_min"]
                .round(1)
                .tolist()
            ),

            "symbol": "circle",

            "symbolSize": 8,

            "lineStyle": {
                "width": 4
            }
        }
    ]
}


st.echarts_chart(
    temperature_options,
    height=400,
    width="stretch"
)


# -------------------------
# Wind Gust
# -------------------------

st.subheader("💨 Maximum Wind Gust")


wind_options = {

    "tooltip": {
        "trigger": "axis"
    },

    "xAxis": {
        "type": "category",
        "data": chart_dates
    },

    "yAxis": {
        "type": "value",
        "name": "km/h"
    },

    "series": [
        {
            "name": "Wind Gust",

            "type": "line",

            "smooth": True,

            "data": (
                chart_df["wind_gust_max"]
                .round(1)
                .tolist()
            ),

            "symbol": "circle",

            "symbolSize": 9,

            "lineStyle": {
                "width": 5
            },

            "areaStyle": {
                "opacity": 0.1
            }
        }
    ]
}


st.echarts_chart(
    wind_options,
    height=380,
    width="stretch"
)


# -------------------------
# Precipitation
# -------------------------

st.subheader("🌧️ Precipitation")


rain_options = {

    "tooltip": {
        "trigger": "axis"
    },

    "xAxis": {
        "type": "category",
        "data": chart_dates
    },

    "yAxis": {
        "type": "value",
        "name": "mm"
    },

    "series": [
        {
            "name": "Precipitation",

            "type": "bar",

            "data": (
                chart_df["precipitation"]
                .round(1)
                .tolist()
            ),

            "barWidth": "55%",

            "itemStyle": {
                "borderRadius": [
                    6,
                    6,
                    0,
                    0
                ]
            }
        }
    ]
}


st.echarts_chart(
    rain_options,
    height=380,
    width="stretch"
)


# -------------------------
# Precipitation Probability
# -------------------------

st.subheader("☔ Precipitation Probability")


probability_options = {

    "tooltip": {
        "trigger": "axis"
    },

    "xAxis": {
        "type": "category",
        "data": chart_dates
    },

    "yAxis": {
        "type": "value",
        "name": "%",
        "min": 0,
        "max": 100
    },

    "series": [
        {
            "name": "Rain Probability",

            "type": "line",

            "smooth": True,

            "data": (
                chart_df[
                    "precipitation_probability"
                ]
                .round(1)
                .tolist()
            ),

            "symbol": "circle",

            "symbolSize": 8,

            "lineStyle": {
                "width": 4
            },

            "areaStyle": {
                "opacity": 0.2
            }
        }
    ]
}


st.echarts_chart(
    probability_options,
    height=380,
    width="stretch"
)


st.divider()


# -------------------------
# Data table
# -------------------------

st.subheader("📋 Weather Forecast Data")


display_columns = [
    "city",
    "forecast_date",
    "temperature_max",
    "temperature_min",
    "precipitation",
    "precipitation_probability",
    "wind_speed_max",
    "wind_gust_max",
    "risk_score",
    "risk_level"
]


st.dataframe(
    filtered_df[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)