import queue
import os
from datetime import datetime
from typing import Set, Optional
import logging
from ..core.paths import get_log_path

class Logger:
    def __init__(self):
        self.message_queue: queue.Queue = queue.Queue()
        self.websocket_clients: Set = set()
        self.MAX_LOG_SIZE: int = 10 * 1024 * 1024  # 10 MB
        self.setup_logging()

    def setup_logging(self):
        """Налаштування системи логування"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Додаємо handler для файлу
        file_handler = logging.FileHandler(get_log_path(), encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        )
        logging.getLogger().addHandler(file_handler)

    def log_message(self, message: str, level: str = "INFO") -> None:
        """Логування повідомлень"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] [{level}] {message}"
        
        # Логуємо через стандартний logging
        if level == "ERROR":
            logging.error(message)
        elif level == "WARNING":
            logging.warning(message)
        elif level == "DEBUG":
            logging.debug(message)
        else:
            logging.info(message)
        
        # Зберігаємо в файл
        self._write_to_file(formatted_message)
        
        # Відправляємо в чергу для веб-інтерфейсу
        self.message_queue.put(formatted_message)
        
        # Відправляємо WebSocket клієнтам
        self._send_to_websocket_clients(formatted_message)
        
        # Перевіряємо розмір лог файлу
        self._check_log_size()

    def _write_to_file(self, message: str) -> None:
        """Запис у файл логів"""
        try:
            with open(get_log_path(), 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"Помилка запису логу: {e}")

    def _send_to_websocket_clients(self, message: str) -> None:
        """Відправка повідомлення WebSocket клієнтам"""
        clients_copy = self.websocket_clients.copy()
        for client in clients_copy:
            try:
                client.send(message)
            except Exception:
                if client in self.websocket_clients:
                    self.websocket_clients.remove(client)

    def _check_log_size(self) -> None:
        """Перевірка розміру лог файлу"""
        try:
            log_path = get_log_path()
            if os.path.exists(log_path) and os.path.getsize(log_path) > self.MAX_LOG_SIZE:
                # Створюємо архівний файл
                archive_name = os.path.join(
                    os.path.dirname(log_path),
                    f"bot_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
                os.rename(log_path, archive_name)
                logging.info(f"Створено архів логів: {archive_name}")
        except Exception as e:
            print(f"Помилка ротації логів: {e}")

    def get_logs(self) -> str:
        """Отримати всі логи"""
        try:
            log_path = get_log_path()
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            logging.error(f"Помилка читання логів: {e}")
            return ""

    def clear_logs(self) -> None:
        """Очистити файл логів"""
        try:
            with open(get_log_path(), 'w', encoding='utf-8') as f:
                f.write("")
            logging.info("Логи очищено")
        except Exception as e:
            logging.error(f"Помилка очищення логів: {e}")

    def log_error(self, error_message: str, exception: Optional[Exception] = None) -> None:
        """Логування помилок"""
        if exception:
            error_details = f"""
Exception: {str(exception)}
Traceback:
  {str(exception.__traceback__.tb_frame)}
  {str(exception.__traceback__.tb_lineno)}

Stack trace:
  {exception.__traceback__}
"""
            self.log_message(f"{error_message}\n{error_details}", "ERROR")
        else:
            self.log_message(error_message, "ERROR")

# Створюємо глобальний екземпляр логера
logger = Logger()

# Функції для зручного доступу
def log_to_console(message: str, level: str = "INFO") -> None:
    logger.log_message(message, level)

def log_error(message: str, exception: Optional[Exception] = None) -> None:
    logger.log_error(message, exception)

def get_logs() -> str:
    return logger.get_logs()

def clear_logs() -> None:
    logger.clear_logs()