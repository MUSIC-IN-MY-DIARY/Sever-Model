FROM apache/airflow:slim-latest-python3.9

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip

USER airflow

RUN pip install redis requests lxml

COPY data/dags /opt/airflow/dags

CMD ["bash", "-c", "airflow db init && airflow webserver --port 8080"]


