from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://myuser:Password123%21@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version()")
        )

        print(result.fetchone())



if __name__ == "__main__":
    test_connection()






# psql -U myuser -d mydb -h localhost