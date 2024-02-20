import json
import logging
from db_config import get_engine
from sqlalchemy.orm import sessionmaker
from alchemy_json_models import AccruedCommissions, RepoDocuments, TradeDocuments, FinancialInstrumentsMovement, MoneyMovement
from json_mappings import mappings
import json
import os, shutil
from pathlib import Path
import datetime


class TLProcessor:
    def __init__(self, json_file_path, dest_dir="/opt/airflow/dags/temp/reports/"):
        self.json_file_path = json_file_path
        self.dest_dir = dest_dir
        logging.info(f"путь к файлу: {self.json_file_path}")
        engine = get_engine()
        self.Session = sessionmaker(bind=engine)

    def transform_and_load_to_db(self):
        if not os.path.exists(self.json_file_path):
            logging.error("В папке true_inbox нет нужного файла.")
            raise FileNotFoundError("В папке true_inbox нет нужного файла.")

        with open(self.json_file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
            report_period = data["ПараметрыОтчета"]["КонецПериода"]
            acc_num = data["ПараметрыОтчета"]["ЛицевойСчет"]

            logging.info(report_period)

        try:
            with self.Session() as session:
                for model_name, model_info in mappings.items():
                    model_class = globals()[model_name]
                    json_key = model_info['json_key']
                    for chunk in data[json_key]:
                        model_data = {model_field: chunk.get(json_field, None) for model_field, json_field in
                                      model_info['mapping'].items()}
                        model_data['report_period'] = report_period
                        model_instance = model_class(**model_data)
                        session.add(model_instance)
                session.commit()
                self.move_file(report_period, acc_num)
        except Exception as e:
            logging.error(f"Ошибка при работе с базой данных: {e}")
            raise

    def rename_file(self, date_str, acc_num):
        try:
            # Создаем объект Path для удобства работы с путями и файлами
            original_path = Path(self.json_file_path)

            # Получаем расширение исходного файла
            file_extension = original_path.suffix

            # Формируем новое имя файла, добавляя дату и сохраняя расширение
            new_file_name = f"{acc_num}_{date_str[:10]}{file_extension}"

            # Создаем новый путь к файлу в том же каталоге, что и исходный файл
            new_file_path = original_path.parent / new_file_name

            # Переименовываем файл
            os.rename(self.json_file_path, new_file_path)

            logging.info(f"Файл был переименован и теперь находится по пути: {new_file_path}")
            # Возвращаем новый путь к файлу для дальнейшего использования
            return new_file_path
        except Exception as e:
            logging.error(f"Ошибка при переименовании файла: {e}")
            raise


    def move_file(self, report_period, acc_num):
        try:
            self.json_file_path = self.rename_file(report_period, acc_num)
            self.dest_dir = f"{self.dest_dir}/{report_period[:7]}"
            os.makedirs(self.dest_dir, exist_ok=True)
            shutil.move(str(self.json_file_path), str(self.dest_dir))
            logging.info(f"Файл {self.json_file_path} успешно перемещен в {self.dest_dir}")
        except Exception as e:
            logging.error(f"Ошибка при перемещении файла: {e}")
            raise

