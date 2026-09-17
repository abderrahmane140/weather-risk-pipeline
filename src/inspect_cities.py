import pandas as pd

def inspect_cities():

    file_path = "data/worldcities.csv"

    df= pd.read_csv(file_path)

    moroccain_citys = df[df["country"] == "Morocco"]

    print("number of cities in morroco:")
    print(len(moroccain_citys))

    print("\nmorocain citys")
    print(moroccain_citys)

    print("\n Columns")
    print(moroccain_citys.columns.tolist())

    print("\n fist 5 rows:")
    print(moroccain_citys.head())

    print("\nData types:")
    print(moroccain_citys.dtypes)

    print("\n Missing values:")
    print(moroccain_citys.isnull().sum())






if __name__ == "__main__":
    inspect_cities()