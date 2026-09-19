import pandas as pd
from sqlalchemy import text

from database import engine


def load_gold_data():
    df = pd.read_csv("gold/weather_gold.csv")

    with engine.begin() as connection:
        for _, row in df.iterrows():

            # Insert city if it does not already exist
            city_result = connection.execute(
                text(
                    """
                    INSERT INTO cities (name, latitude, longitude)
                    VALUES (:name, :latitude, :longitude)
                    ON CONFLICT (name, latitude, longitude)
                    DO UPDATE SET name = EXCLUDED.name
                    RETURNING id;
                    """
                ),
                {
                    "name": row["city"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                }
            )

            city_id = city_result.scalar_one()

            # Insert or update weather forecast
            connection.execute(
                text(
                    """
                    INSERT INTO weather_forecasts (
                        city_id,
                        forecast_date,
                        temperature_max,
                        temperature_min,
                        precipitation,
                        precipitation_probability,
                        wind_speed_max,
                        wind_gust_max,
                        weather_code,
                        temperature_category,
                        rain_category,
                        wind_category,
                        temperature_risk,
                        rain_risk,
                        wind_risk,
                        risk_score,
                        risk_level
                    )
                    VALUES (
                        :city_id,
                        :forecast_date,
                        :temperature_max,
                        :temperature_min,
                        :precipitation,
                        :precipitation_probability,
                        :wind_speed_max,
                        :wind_gust_max,
                        :weather_code,
                        :temperature_category,
                        :rain_category,
                        :wind_category,
                        :temperature_risk,
                        :rain_risk,
                        :wind_risk,
                        :risk_score,
                        :risk_level
                    )
                    ON CONFLICT (city_id, forecast_date)
                    DO UPDATE SET
                        temperature_max = EXCLUDED.temperature_max,
                        temperature_min = EXCLUDED.temperature_min,
                        precipitation = EXCLUDED.precipitation,
                        precipitation_probability = EXCLUDED.precipitation_probability,
                        wind_speed_max = EXCLUDED.wind_speed_max,
                        wind_gust_max = EXCLUDED.wind_gust_max,
                        weather_code = EXCLUDED.weather_code,
                        temperature_category = EXCLUDED.temperature_category,
                        rain_category = EXCLUDED.rain_category,
                        wind_category = EXCLUDED.wind_category,
                        temperature_risk = EXCLUDED.temperature_risk,
                        rain_risk = EXCLUDED.rain_risk,
                        wind_risk = EXCLUDED.wind_risk,
                        risk_score = EXCLUDED.risk_score,
                        risk_level = EXCLUDED.risk_level;
                    """
                ),
                {
                    "city_id": city_id,
                    "forecast_date": row["date"],
                    "temperature_max": row["temperature_max"],
                    "temperature_min": row["temperature_min"],
                    "precipitation": row["precipitation"],
                    "precipitation_probability": row["precipitation_probability"],
                    "wind_speed_max": row["wind_speed_max"],
                    "wind_gust_max": row["wind_gust_max"],
                    "weather_code": row["weather_code"],
                    "temperature_category": row["temperature_category"],
                    "rain_category": row["rain_category"],
                    "wind_category": row["wind_category"],
                    "temperature_risk": row["temperature_risk"],
                    "rain_risk": row["rain_risk"],
                    "wind_risk": row["wind_risk"],
                    "risk_score": row["risk_score"],
                    "risk_level": row["risk_level"],
                }
            )

    print("Gold data loaded successfully into PostgreSQL.")


if __name__ == "__main__":
    load_gold_data()