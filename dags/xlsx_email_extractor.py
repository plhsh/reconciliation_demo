import imaplib
import email
import os
from email.header import decode_header
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class XlsxEmailExtractor:
    def __init__(self, username, password, imap_url):
        self.username = username
        self.password = password
        self.imap_url = imap_url
        self.attachments_folder = "/opt/airflow/dags/data/attachments_folder"
        self.connection = None
        self.filepath = None
        self._create_directory(self.attachments_folder)

    def _create_directory(self, path):
        """Пытается создать директорию, если она не существует."""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            logging.error(f"Ошибка при создании директории {path}: {e}")
            raise

    @staticmethod
    def decode_mime_words(s):
        return u''.join(word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
                        for word, encoding in email.header.decode_header(s))

    def connect(self):
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_url)
            self.connection.login(self.username, self.password)
            self.connection.select('inbox')
            logging.info("Успешное подключение к почтовому ящику.")
        except Exception as e:
            logging.error(f"Ошибка подключения: {e}")

    def fetch_attachments(self, file_extension):
        try:
            result, data = self.connection.search(None, 'ALL')
            if result == 'OK':
                for num in reversed(data[0].split()):
                    result, data = self.connection.fetch(num, '(RFC822)')
                    if result == 'OK':
                        raw_email = data[0][1]
                        email_message = email.message_from_bytes(raw_email)
                        for part in email_message.walk():
                            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                                continue
                            filename = part.get_filename()
                            if filename:
                                decoded_filename = self.decode_mime_words(filename)
                                logging.info(
                                    f"Обнаружено вложение: {decoded_filename}")  # Для проверки получения имени файла
                                if decoded_filename.lower().endswith(file_extension):
                                    logging.info(f"Найдено вложение: {decoded_filename}")
                                    self.filepath = os.path.join(self.attachments_folder, decoded_filename)
                                    with open(self.filepath, 'wb') as f:
                                        f.write(part.get_payload(decode=True))
                                    logging.info(f"Вложение сохранено: {self.filepath}")
                                    return self.filepath

            else:
                logging.warning("Ошибка поиска сообщений.")
        except Exception as e:
            logging.error(f"Ошибка при извлечении вложений: {e}")

    def disconnect(self):
        try:
            self.connection.logout()
            logging.info("Отключение от почтового ящика выполнено.")
        except Exception as e:
            logging.error(f"Ошибка при отключении: {e}")

