import pandas as pd
from pathlib import Path

from load_postgres import  load_gold_data


def temperature_category(temp):
    if temp < 15:
        return "Cold"
    elif temp < 30:
        return "Normal"
    elif temp < 35:
        return "Hot"
    else:
        return "Extreme"


def rain_category(rain):
    if rain == 0:
        return "None"
    elif rain < 2.5:
        return "Light"
    elif rain < 10:
        return "Moderate"
    elif rain < 30:
        return "Heavy"
    else:
        return "Very Heavy"


def wind_category(wind):
    if wind < 20:
        return "Low"
    elif wind < 40:
        return "Moderate"
    elif wind < 60:
        return "High"
    else:
        return "Extreme"


def temperature_risk(temp):
    if temp < 5 or temp > 40:
        return 100
    elif temp < 10 or temp > 35:
        return 70
    elif temp < 15 or temp > 30:
        return 40
    else:
        return 10


def rain_risk(rain):
    if rain == 0:
        return 0
    elif rain < 2.5:
        return 20
    elif rain < 10:
        return 50
    elif rain < 30:
        return 80
    else:
        return 100


def wind_risk(wind):
    if wind < 20:
        return 10
    elif wind < 40:
        return 40
    elif wind < 60:
        return 70
    else:
        return 100


def risk_level(score):
    if score < 20:
        return "Very Low"
    elif score < 40:
        return "Low"
    elif score < 60:
        return "Moderate"
    elif score < 80:
        return "High"
    else:
        return "Very High"


def build_gold():
    df = pd.read_csv("silver/weather_clean.csv")


    df["temperature_category"] = df["temperature_max"].apply(
        temperature_category
    )

    df["rain_category"] = df["precipitation"].apply(
        rain_category
    )

    df["wind_category"] = df["wind_gust_max"].apply(
        wind_category
    )


    df["temperature_risk"] = df["temperature_max"].apply(
        temperature_risk
    )

    df["rain_risk"] = df["precipitation"].apply(
        rain_risk
    )

    df["wind_risk"] = df["wind_gust_max"].apply(
        wind_risk
    )

    df["risk_score"] = (
        df["temperature_risk"] * 0.25
        + df["rain_risk"] * 0.35
        + df["wind_risk"] * 0.40
    ).round(2)


    df["risk_level"] = df["risk_score"].apply(
        risk_level
    )

    gold_dir = Path("gold")
    gold_dir.mkdir(exist_ok=True)

    output_file = gold_dir / "weather_gold.csv"


    df.to_csv(
        output_file,
        index=False
    )

    print(df.head())
    print()
    print(f"Rows: {len(df)}")
    print(f"Cities: {df['city'].nunique()}")
    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    build_gold()

# future engineering : transformations