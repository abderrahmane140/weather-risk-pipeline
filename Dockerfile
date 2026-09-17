ARG AIRFLOW_VERSION=2.9.3

FROM apache/airflow:${AIRFLOW_VERSION}-python3.11

# Copy the Airflow-only dependencies
COPY --chown=airflow:root requirements-airflow.txt /requirements-airflow.txt

# Install packages using versions compatible with Airflow 2.9.3
RUN pip install --no-cache-dir \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.11.txt" \
    -r /requirements-airflow.txt

# Copy your Weather Risk Pipeline DAGs into Airflow
COPY --chown=airflow:root dags/ /opt/airflow/dags/