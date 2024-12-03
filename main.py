import os
import sys

def get_base_path():
    """Отримати шлях до папки з ресурсами"""
    if getattr(sys, 'frozen', False):
        # Якщо запущено як exe
        return sys._MEIPASS
    # Якщо запущено як python скрипт
    return os.path.dirname(os.path.abspath(__file__))

def setup_environment():
    """Налаштувати шляхи до ресурсів"""
    base_path = get_base_path()
    os.environ['BASE_PATH'] = base_path
    
    # Додаємо шляхи до ресурсів
    templates_path = os.path.join(base_path, 'templates')
    static_path = os.path.join(base_path, 'static')
    config_path = os.path.join(base_path, 'config.json')
    
    return templates_path, static_path, config_path

def main():
    try:
        # Налаштовуємо шляхи
        templates_path, static_path, config_path = setup_environment()
        
        # Імпортуємо після налаштування шляхів
        from threading import Thread
        from src.gui.web_server import app
        from src.gui.app import QApplication, create_window, QUrl, sys, QSystemTrayIcon, QMessageBox
        from src.core.config import load_config
        from src.bot.bot_manager import start_bot

        # Налаштовуємо Flask
        app.template_folder = templates_path
        app.static_folder = static_path
        
        # Запускаємо Flask у окремому потоці
        def run_flask():
            app.run(port=5000, threaded=True)
            
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Автоматично запускаємо бота
        config = load_config()
        if config['telegram_token']:
            start_bot(config['telegram_token'])

        # Створюємо Qt додаток
        qt_app = QApplication(sys.argv)
        qt_app.setQuitOnLastWindowClosed(False)
        
        window = create_window()
        sys.exit(qt_app.exec())
        
    except Exception as e:
        print(f"Помилка запуску програми: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 