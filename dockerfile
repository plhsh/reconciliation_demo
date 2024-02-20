FROM apache/airflow:2.8.1

# Установка дополнительных зависимостей
RUN pip install --no-cache-dir openpyxl
