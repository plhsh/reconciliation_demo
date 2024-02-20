from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from json_extractor import JsonExtractor
from json_tl_processor import TLProcessor

today = datetime.combine(datetime.today(), datetime.min.time())
mock_url = 'https://httpbin.org/json'


def download_and_save_json(**kwargs):
    url = kwargs.get('url')
    downloader = JsonExtractor(url)
    file_path = downloader.download_mock_and_return_oldest_real_file()
    kwargs['ti'].xcom_push(key='file_path', value=file_path)


def transform_load_to_db(**kwargs):
    ti = kwargs['ti']
    # Получение пути к файлу из XCom
    file_path = ti.xcom_pull(task_ids="extract_json", key="file_path")
    processor = TLProcessor(file_path)
    processor.transform_and_load_to_db()


default_args = {
    'owner': 'airflow',
    'start_date': today,
}

with DAG('json_etl_dag',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    download_task = PythonOperator(
        task_id='extract_json',
        python_callable=download_and_save_json,
        op_kwargs={'url': mock_url},
    )
    transform_load_task = PythonOperator(
        task_id='transform_load',
        python_callable=transform_load_to_db,
    )

    download_task >> transform_load_task
