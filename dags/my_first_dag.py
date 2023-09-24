from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils.extract import parse_from_prothomalo, parse_from_jugantor, parse_from_kalerkantho
from utils.helper import transform_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_Pipeline',
    default_args=default_args,
    schedule_interval='*/60 * * * *',  # Execute every minute
    catchup=False
)

# Define the tasks for data extraction
task_extract_prothomalo = PythonOperator(
    task_id='extract_prothomalo',
    python_callable=parse_from_prothomalo,
    dag=dag
)

task_extract_jugantor = PythonOperator(
    task_id='extract_jugantor',
    python_callable=parse_from_jugantor,
    dag=dag
)

task_extract_kalerkantho = PythonOperator(
    task_id='extract_kalerkantho',
    python_callable=parse_from_kalerkantho,
    dag=dag
)

# Define the transformation task
task_transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

# Set up the dependencies
[
    task_extract_prothomalo, task_extract_jugantor, task_extract_kalerkantho
] >> task_transform_data