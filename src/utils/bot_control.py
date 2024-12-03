import os
import sys
from datetime import datetime
from ..core.logger import get_logs

def shutdown_program():
    """Завершити роботу програми"""
    try:
        # Логуємо завершення роботи
        from ..core.logger import log_to_console
        log_to_console("Завершення роботи програми...")
        
        # Зупиняємо бота якщо він запущений
        from ..bot.bot_manager import stop_bot
        stop_bot()
        
        # Завершуємо програму
        os._exit(0)
    except Exception as e:
        print(f"Помилка завершення програми: {e}")
        sys.exit(1)

def get_log_file():
    """Отримати файл логів"""
    try:
        # Створюємо тимчасовий файл з унікальним ім'ям
        log_filename = f"bot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Отримуємо всі логи
        logs = get_logs()
        if not logs:
            return None
            
        # Записуємо логи в тимчасовий файл
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write(logs)
        
        return log_filename
            
    except Exception as e:
        print(f"Помилка створення лог-файлу: {e}")
        if os.path.exists(log_filename):
            os.remove(log_filename)
        return None 