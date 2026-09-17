import json
from datetime import date
from pathlib import Path

import pandas as pd


def build_silver():
    today = date.today().isoformat()

    bronze_file = Path(
        f"bronze/weather/{today}/weather_morocco.json"
    )

    with open(bronze_file, "r", encoding="utf-8") as file:
        bronze_data = json.load(file)

    rows = []

    for city_data in bronze_data["cities"]:
        city = city_data["city"]
        latitude = city_data["requested_latitude"]
        longitude = city_data["requested_longitude"]

        weather = city_data["weather"]
        daily = weather["daily"]

        for index, weather_date in enumerate(daily["time"]):
            rows.append({
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
                "date": weather_date,
                "temperature_max": daily["temperature_2m_max"][index],
                "temperature_min": daily["temperature_2m_min"][index],
                "precipitation": daily["precipitation_sum"][index],
                "precipitation_probability": daily[
                    "precipitation_probability_max"
                ][index],
                "wind_speed_max": daily["wind_speed_10m_max"][index],
                "wind_gust_max": daily["wind_gusts_10m_max"][index],
                "weather_code": daily["weather_code"][index],
            })

    df = pd.DataFrame(rows)

    # Clean date
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicate city/date rows
    df = df.drop_duplicates(
        subset=["city", "date"]
    )

    # Remove rows with important missing values
    df = df.dropna(
        subset=[
            "city",
            "date",
            "temperature_max",
            "temperature_min",
        ]
    )

    # Remove impossible values
    df = df[df["precipitation"] >= 0]

    df = df[
        df["precipitation_probability"].between(
            0,
            100,
        )
    ]

    df = df[df["wind_speed_max"] >= 0]
    df = df[df["wind_gust_max"] >= 0]

    silver_dir = Path("silver")
    silver_dir.mkdir(exist_ok=True)

    output_file = silver_dir / "weather_clean.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    print(df.head())
    print()
    print(f"Rows: {len(df)}")
    print(f"Cities: {df['city'].nunique()}")
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    build_silver()