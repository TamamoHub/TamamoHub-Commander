import os
import sys
from datetime import datetime
from ..core.logger import get_logs, log_to_console, log_error

def shutdown_program():
    """Завершити роботу програми"""
    try:
        log_to_console("Initiating program shutdown sequence...")
        
        # Зупиняємо бота якщо він запущений
        from ..bot.bot_manager import stop_bot
        log_to_console("Stopping Telegram bot...")
        stop_bot()
        
        # Зупиняємо Flask сервер
        log_to_console("Stopping Flask server...")
        import requests
        try:
            requests.get('http://localhost:5000/shutdown', timeout=1)
            log_to_console("Flask server stopped successfully")
        except requests.exceptions.RequestException as e:
            log_error("Error stopping Flask server", e)
            
        # Даємо час на завершення всіх процесів
        import time
        log_to_console("Waiting for processes to finish...")
        time.sleep(1)
        
        # Завершуємо програму
        log_to_console("Program shutdown complete")
        os._exit(0)
    except Exception as e:
        log_error("Critical error during program shutdown", e)
        sys.exit(1)

def get_log_file():
    """Отримати файл логів"""
    log_filename = None
    try:
        # Створюємо тимчасовий файл з унікальним ім'ям
        log_filename = f"bot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        log_to_console(f"Creating temporary log file: {log_filename}")
        
        # Отримуємо всі логи
        logs = get_logs()
        if not logs:
            log_to_console("No logs available", "WARNING")
            return None
            
        # Записуємо логи в тимчасовий файл
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write(logs)
        
        log_to_console(f"Log file created successfully: {log_filename}")
        return log_filename
            
    except Exception as e:
        log_error("Error creating log file", e)
        if log_filename and os.path.exists(log_filename):
            try:
                os.remove(log_filename)
                log_to_console(f"Cleaned up temporary log file: {log_filename}")
            except Exception as cleanup_error:
                log_error("Error cleaning up temporary log file", cleanup_error)
        return None 