from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from alchemy_json_models import main


with DAG('json_init_db_dag',
         start_date=days_ago(1),
         schedule_interval='@once',
         is_paused_upon_creation=False
         ) as dag:
    init_db_task = PythonOperator(
        task_id='init_db',
        python_callable=main,
    )

