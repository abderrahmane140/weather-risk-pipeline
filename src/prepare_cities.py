import pandas as pd


def prepare_morocco_cities():
    df = pd.read_csv("data/worldcities.csv")

    morocco_cities = df[
        df["country"] == "Morocco"
    ].copy()

    morocco_cities = morocco_cities[
        ["city", "lat", "lng"]
    ]

    morocco_cities = morocco_cities.drop_duplicates(
        subset=["city", "lat", "lng"]
    )

    morocco_cities.to_csv(
        "data/morocco_cities.csv",
        index=False
    )

    print(f"Moroccan cities: {len(morocco_cities)}")
    print(morocco_cities.head())


if __name__ == "__main__":
    prepare_morocco_cities()