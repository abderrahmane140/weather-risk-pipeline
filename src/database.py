import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "myuser"),
    password=os.getenv("DB_PASSWORD", "Password123!"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "mydb"),
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user;")
        )

        print(result.fetchone())


if __name__ == "__main__":
    test_connection()