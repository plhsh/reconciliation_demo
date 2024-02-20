from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from xlsx_tl_processor import main
from xlsx_email_extractor import XlsxEmailExtractor
from email_config import email_credentials


def download_and_save_xlsx(**kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    imap_url = kwargs.get('imap_url')
    email_client = XlsxEmailExtractor(username, password, imap_url)
    email_client.connect()
    file_path = email_client.fetch_attachments('.xlsx')
    email_client.disconnect()
    kwargs['ti'].xcom_push(key='file_path', value=file_path)


def xlsx_transform_load_to_db(**kwargs):
    ti = kwargs['ti']
    # Получение пути к файлу из XCom
    file_path = ti.xcom_pull(task_ids="extract_xlsx", key="file_path")
    main(file_path)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG('xlsx_etl_dag',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    download_task = PythonOperator(
        task_id='extract_xlsx',
        python_callable=download_and_save_xlsx,
        op_kwargs=email_credentials
    )
    xlsx_transform_load_task = PythonOperator(
        task_id='xlsx_transform_load',
        python_callable=xlsx_transform_load_to_db,
    )

    download_task >> xlsx_transform_load_task
