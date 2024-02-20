from db_config import get_engine
import pandas as pd
from datetime import datetime
from xlsx_mappings import tables_info
import os
import shutil
import logging

import os
from pathlib import Path


def rename_file(original_file_path, acc_num, date_str):
    # Создаем объект Path для удобства работы с путями и файлами
    original_path = Path(original_file_path)

    # Получаем расширение исходного файла
    file_extension = original_path.suffix

    # Формируем новое имя файла, добавляя дату и сохраняя расширение
    new_file_name = f"{acc_num}_{date_str[:10]}{file_extension}"

    # Создаем новый путь к файлу в том же каталоге, что и исходный файл
    new_file_path = original_path.parent / new_file_name

    # Переименовываем файл
    os.rename(original_file_path, new_file_path)

    logging.info(f"Файл был переименован и теперь находится по пути: {new_file_path}")
    # Возвращаем новый путь к файлу для дальнейшего использования
    return new_file_path

def move_file(file_path, report_period):
    try:
        dest_dir = f"/opt/airflow/dags/temp/reports/{report_period[:7]}"
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(str(file_path), str(dest_dir))
        logging.info(f"Файл {file_path} успешно перемещен в {dest_dir}")
    except Exception as e:
        logging.error(f"Ошибка при перемещении файла: {e}")
        raise

def convert_date(date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    return datetime.strftime(date_obj, "%Y-%m-%d %H:%M:%S")


def process_table(df_slice, column_names, date_columns, table_name, engine):
    """
    Обрабатывает срез DataFrame, присваивая новые имена столбцам,
    преобразует текстовые даты в datetime и загружает данные в базу данных.
    """
    df_slice.columns = column_names

    # Преобразование столбцов с датами
    for date_column in date_columns:
        df_slice[date_column] = pd.to_datetime(df_slice[date_column], dayfirst=True)
        df_slice[date_column] = df_slice[date_column].dt.strftime(
            '%Y-%m-%d %H:%M:%S')  # Опционально, если нужно отформатировать дату как строку

    # запись в бд
    df_slice.to_sql(table_name, con=engine, if_exists='append', index=False)


def main(file_path):
    sheet_name = 'Лист1'
    all_data = pd.read_excel(file_path, sheet_name=sheet_name)

    report_period = convert_date(all_data.iat[2, 1].split('по ')[1])
    acc_no = all_data.iat[0, 1].split('счету ')[1]

    # Идентификация строк с заголовками и определение концов таблиц
    header_titles = ['1. Движение денежных средств:', '2. Движение финансовых инструментов:', '3. Покупка / продажа:',
                     '4. РЕПО:', '5. Приказы:', '6. Плановый остаток:', '7. Начисленные комиссии:']
    header_rows = all_data[all_data.iloc[:, 1].isin(header_titles)].index
    last_table_end_index = all_data.iloc[header_rows[-1]:].last_valid_index() - 8
    table_starts = header_rows
    table_ends = header_rows[1:].append(pd.Index([last_table_end_index]))

    engine = get_engine()

    for table_info in tables_info:
        start = table_starts[table_info['index']]
        end = table_ends[table_info['index']]
        # Пропускаем строки заголовка и шапки таблицы в соответствии с 'header_skip'
        table_data = all_data.iloc[start + table_info['header_skip']:end, table_info['column_range']]
        table_data["report_period"] = report_period
        process_table(table_data, table_info['columns'], table_info['date_columns'], table_info['table_name'], engine)

    new_file_path = rename_file(file_path, acc_no, report_period)
    move_file(new_file_path, report_period)


if __name__ == '__main__':
    main()
