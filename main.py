import os
import sys
from src.core.logger import log_to_console, log_error
import logging

# Налаштовуємо фільтр для логів
class NoDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.DEBUG

# Налаштовуємо базове логування
logging.basicConfig(level=logging.DEBUG)  # Встановлюємо найнижчий рівень, щоб захопити всі логи
logger = logging.getLogger()

# Додаємо фільтр до всіх хендлерів
for handler in logger.handlers:
    handler.addFilter(NoDebugFilter())

def get_base_path():
    """Отримати шлях до папки з ресурсами"""
    if getattr(sys, 'frozen', False):
        # Якщо запущено як exe
        return sys._MEIPASS
    # Якщо запущено як python скрипт
    return os.path.dirname(os.path.abspath(__file__))

def setup_environment():
    """Налаштувати шляхи до ресурсів"""
    try:
        base_path = get_base_path()
        os.environ['BASE_PATH'] = base_path
        
        # Додаємо шляхи до ресурсів
        templates_path = os.path.join(base_path, 'templates')
        static_path = os.path.join(base_path, 'static')
        
        log_to_console(f"Environment setup completed. Base path: {base_path}")
        return templates_path, static_path
    except Exception as e:
        log_error("Failed to setup environment", e)
        raise

def main():
    try:
        log_to_console("Starting application...")
        
        # Налаштовуємо шляхи
        templates_path, static_path = setup_environment()
        
        # Імпортуємо після налаштування шляхів
        from threading import Thread
        from src.gui.web_server import app
        from src.gui.app import QApplication, create_window, QUrl, sys, QSystemTrayIcon, QMessageBox
        from src.core.config import load_config
        from src.bot.bot_manager import start_bot

        # Налаштовуємо Flask
        app.template_folder = templates_path
        app.static_folder = static_path
        log_to_console("Flask configuration completed")
        
        # Запускаємо Flask у окремому потоці
        def run_flask():
            try:
                log_to_console("Starting Flask server...")
                app.run(port=5000, threaded=True)
            except Exception as e:
                log_error("Flask server error", e)
            
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Автоматично запускаємо бота
        config = load_config()
        if config['telegram_token']:
            log_to_console("Starting Telegram bot...")
            start_bot(config['telegram_token'])
        else:
            log_to_console("No Telegram token found, skipping bot start", "WARNING")

        # Створюємо Qt додаток
        log_to_console("Initializing Qt application...")
        qt_app = QApplication(sys.argv)
        qt_app.setQuitOnLastWindowClosed(False)
        
        window = create_window()
        log_to_console("Application started successfully")
        sys.exit(qt_app.exec())
        
    except Exception as e:
        log_error("Critical application error", e)
        sys.exit(1)

if __name__ == '__main__':
    main() 