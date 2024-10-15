FROM apache/airflow:slim-latest-python3.9

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip

USER airflow

RUN pip install redis requests lxml

COPY data/dags /opt/airflow/dags

COPY .env /opt/airflow/.env

CMD ["bash", "-c", "source /opt/airflow/.env && airflow db init && airflow users create --username $ADMIN_USERNAME --password $ADMIN_PASSWORD --firstname Admin --lastname User --role Admin --email admin@example.com && airflow webserver --port 8080"]


