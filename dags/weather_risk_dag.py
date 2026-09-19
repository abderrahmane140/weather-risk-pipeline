import sys
from datetime import timedelta

import pendulum

from airflow.decorators import dag, task


sys.path.insert(
    0,
    "/opt/airflow/src"
)


from bronze import extract_morocco_weather
from silver import build_silver
from gold import build_gold
from load_postgres import load_gold_data


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="weather_risk_pipeline",
    description="Morocco weather risk data pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(
        2026,
        9,
        17,
        tz="Africa/Casablanca",
    ),
    catchup=False,
    default_args=default_args,
    tags=[
        "weather",
        "morocco",
        "data-pipeline",
    ],
)
def weather_risk_pipeline():

    @task
    def bronze_task():
        extract_morocco_weather()

    @task
    def silver_task():
        build_silver()

    @task
    def gold_task():
        build_gold()

    @task
    def database_task():
        load_gold_data()

    bronze = bronze_task()
    silver = silver_task()
    gold = gold_task()
    database = database_task()

    bronze >> silver >> gold >> database


weather_risk_pipeline()