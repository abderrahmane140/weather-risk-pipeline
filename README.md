# 🌦️ Weather Risk Pipeline

A Data Engineering project that collects weather forecasts for Moroccan cities, processes the data using a **Bronze → Silver → Gold** architecture, calculates delivery risk, stores the results in PostgreSQL, and displays them in a Streamlit dashboard.

## 🎯 Objective

The goal is to help a delivery company anticipate weather disruptions caused by:

- Heavy rain
- Strong winds
- Extreme temperatures

## 🏗️ Architecture

```text
SimpleMaps
    ↓
Open-Meteo API
    ↓
Bronze
Raw JSON
    ↓
Silver
Clean Data
    ↓
Gold
Risk Data
    ↓
PostgreSQL
    ↓
Streamlit Dashboard
```

Apache Airflow automates the pipeline:

```text
Bronze → Silver → Gold → PostgreSQL
```

## 🛠️ Technologies

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Streamlit
- Apache Airflow
- Docker
- Open-Meteo API

## 📂 Project Structure

```text
weather-risk-pipeline/
├── bronze/
├── silver/
├── gold/
├── dags/
│   └── weather_risk_dag.py
├── data/
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── src/
├── streamlit/
│   └── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🌍 Data Sources

### SimpleMaps

Used to retrieve Moroccan cities with their latitude and longitude.

### Open-Meteo API

Used to retrieve:

- Maximum and minimum temperature
- Precipitation
- Precipitation probability
- Wind speed
- Wind gust
- Weather code

## ⚠️ Risk Calculation

The final risk score is based on:

```text
Temperature Risk = 25%
Rain Risk        = 35%
Wind Risk        = 40%
```

Risk levels:

```text
Very Low
Low
Moderate
High
Very High
```

## 🗄️ Database

The main PostgreSQL tables are:

```text
cities
weather_forecasts
```

Relationship:

```text
City 1 ───── 0..* WeatherForecast
```

## 📊 Dashboard

The Streamlit dashboard includes:

- City filter
- Risk filter
- Date filter
- Temperature metrics
- Wind metrics
- Risk score
- Weather map
- Weather charts
- Data table

Run the dashboard:

```bash
streamlit run streamlit/app.py
```

## 🔄 Apache Airflow

The DAG executes:

```text
bronze_task
    ↓
silver_task
    ↓
gold_task
    ↓
database_task
```

Start Airflow with Docker:

```bash
docker compose up -d
```

Open Airflow:

```text
http://localhost:8080
```

## ▶️ Run Pipeline Manually

```bash
python src/prepare_cities.py
python src/bronze.py
python src/silver.py
python src/gold.py
python src/load_postgres.py
```

## 👨‍💻 Author

**Abderrahmane Bsar**