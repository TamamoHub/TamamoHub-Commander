from cryptography.fernet import Fernet
import os
from ..core.logger import log_to_console
from ..core.paths import get_config_dir

class ConfigEncryption:
    @staticmethod
    def get_key_path():
        """Отримати шлях до файлу ключа"""
        config_dir = get_config_dir()
        return os.path.join(config_dir, '.key')

    @staticmethod
    def generate_key():
        """Згенерувати новий ключ шифрування"""
        return Fernet.generate_key()

    @staticmethod
    def load_or_create_key():
        """Завантажити існуючий ключ або створити новий"""
        key_path = ConfigEncryption.get_key_path()
        try:
            if os.path.exists(key_path):
                with open(key_path, 'rb') as key_file:
                    return key_file.read()
            else:
                key = ConfigEncryption.generate_key()
                os.makedirs(os.path.dirname(key_path), exist_ok=True)
                with open(key_path, 'wb') as key_file:
                    key_file.write(key)
                return key
        except Exception as e:
            log_to_console(f"Помилка роботи з ключем: {str(e)}")
            return None

    @staticmethod
    def encrypt_data(data: str) -> bytes:
        """Зашифрувати дані"""
        try:
            key = ConfigEncryption.load_or_create_key()
            if not key:
                return None
            f = Fernet(key)
            return f.encrypt(data.encode())
        except Exception as e:
            log_to_console(f"Помилка шифрування: {str(e)}")
            return None

    @staticmethod
    def decrypt_data(encrypted_data: bytes) -> str:
        """Розшифрувати дані"""
        try:
            key = ConfigEncryption.load_or_create_key()
            if not key:
                return None
            f = Fernet(key)
            return f.decrypt(encrypted_data).decode()
        except Exception as e:
            log_to_console(f"Помилка розшифрування: {str(e)}")
            return None 