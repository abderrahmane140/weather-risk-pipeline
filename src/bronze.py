import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from weather import get_weather_batch


BATCH_SIZE = 20


def extract_morocco_weather():
    cities = pd.read_csv(
        "data/morocco_cities.csv"
    )

    all_weather = []

    total_cities = len(cities)

    print(
        f"Moroccan cities found: {total_cities}"
    )

    for start in range(
        0,
        total_cities,
        BATCH_SIZE,
    ):
        end = start + BATCH_SIZE

        batch = cities.iloc[start:end]

        batch_number = (
            start // BATCH_SIZE
        ) + 1

        print(
            f"Fetching batch {batch_number} "
            f"({len(batch)} cities)"
        )

        latitudes = batch["lat"].tolist()
        longitudes = batch["lng"].tolist()

        try:
            weather_results = get_weather_batch(
                latitudes,
                longitudes,
            )

            for index, (_, city) in enumerate(
                batch.iterrows()
            ):
                all_weather.append({
                    "city": city["city"],

                    "requested_latitude": float(
                        city["lat"]
                    ),

                    "requested_longitude": float(
                        city["lng"]
                    ),

                    "weather": weather_results[index],
                })

        except Exception as error:
            print(
                f"Error in batch "
                f"{batch_number}: {error}"
            )

        time.sleep(2)

    save_bronze(all_weather)


def save_bronze(all_weather):
    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    bronze_dir = (
        Path("bronze")
        / "weather"
        / today
    )

    bronze_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        bronze_dir
        / "weather_morocco.json"
    )

    data = {
        "extracted_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "total_cities": len(all_weather),

        "cities": all_weather,
    }

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print()
    print(
        f"Extracted cities: "
        f"{len(all_weather)}"
    )

    print(
        f"Saved: {file_path}"
    )


if __name__ == "__main__":
    extract_morocco_weather()