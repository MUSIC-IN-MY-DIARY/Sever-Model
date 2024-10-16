from datetime import datetime, timedelta

from dags.controller import Controller

# airflow
from airflow import DAG
from airflow.operators.python import PythonOperator



default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2019,1,1),
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5),
}

with DAG(
    'user_automation',
    default_args=default_args,
    schedule_interval='@daily',
    catchup = False,
) as dag:

    crawler_task = PythonOperator(
        task_id = 'crawler_task',
        python_callable = Controller().main(),
        dag = dag,
    )

