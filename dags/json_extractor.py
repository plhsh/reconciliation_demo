import requests
import json
import os
from datetime import datetime
import logging


class JsonExtractor:
    def __init__(self, url):
        """
        url: URL для скачивания мок файла.
        true_inbox_folder: Путь к папке с "настоящими" файлами.
        mock_inbox_folder: для скачиваемых мок файлов
        """
        self.url = url
        self.true_inbox_folder = "/opt/airflow/dags/data/json_true_inbox"
        self.mock_inbox_folder = "/opt/airflow/dags/data/json_mock_inbox"
        self._create_directory(self.true_inbox_folder)
        self._create_directory(self.mock_inbox_folder)

    def _create_directory(self, path):
        """Пытается создать директорию, если она не существует."""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            logging.error(f"Ошибка при создании директории {path}: {e}")
            raise

    def download_mock_and_return_oldest_real_file(self):
        """Скачивает мок файл и возвращает путь к наиболее старому "настоящему" файлу."""
        self._download_mock_file()
        oldest_file = self._get_oldest_file_from_true_inbox()
        if oldest_file:
            return os.path.join(self.true_inbox_folder, oldest_file)
        else:
            logging.warning("В папке true_inbox нет файлов.")
            raise FileNotFoundError("В папке true_inbox нет файлов.")

    def _download_mock_file(self):
        """Скачивает мок файл."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Вызывает исключение для кодов ошибок HTTP
            data = response.json()
        except Exception as e:
            logging.error(f"Ошибка при запросе {self.url}: {e}")
            raise

        mock_file_path = os.path.join(self.mock_inbox_folder,
                                      f"mock_json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(mock_file_path, 'w') as file:
            json.dump(data, file)
        logging.info(f"Мок файл успешно скачан: {mock_file_path}")

    def _get_oldest_file_from_true_inbox(self):
        """Возвращает имя наиболее старого файла в папке true_inbox."""
        try:
            files = [f for f in os.listdir(self.true_inbox_folder) if
                     os.path.isfile(os.path.join(self.true_inbox_folder, f))]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.true_inbox_folder, x)))
            if files:
                return files[0]
        except Exception as e:
            logging.error(f"Ошибка при получении наиболее старого файла из {self.true_inbox_folder}: {e}")
            raise
        return None
