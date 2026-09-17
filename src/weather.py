import time
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_batch(
    latitudes,
    longitudes,
    max_retries=5,
):
    params = {
        "latitude": ",".join(map(str, latitudes)),
        "longitude": ",".join(map(str, longitudes)),
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code",
        ]),
        "timezone": "Africa/Casablanca",
        "forecast_days" : 7,
        "cell_selection": 'nearest'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=60
            )

            if response.status_code == 429:
                wait_time = 5 * (attempt + 1)

                print(
                     f"Rate limit reached. "
                     f"Retrying in {wait_time} second..."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict):
                data = [data]

            return data

        except requests.RequestException as error:
            if attempt == max_retries -1:
                raise error

            wait_time = 5 * (attempt + 1)

            print(
                f"Request failed: {error}"
                f"Retrying in {wait_time} second..."
            )

            time.sleep(wait_time)


    raise RuntimeError(
        "Unable to fetch weather data."
    )