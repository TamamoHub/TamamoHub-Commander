import os
import sys

def get_base_path():
    """Отримати базовий шлях програми"""
    if getattr(sys, 'frozen', False):
        # Якщо запущено як exe
        return os.path.dirname(sys.executable)
    # Якщо запущено як python скрипт
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_config_dir():
    """Отримати директорію для конфігураційних файлів"""
    # Використовуємо AppData для Windows
    if os.name == 'nt':
        config_dir = os.path.join(os.environ['APPDATA'], 'TamamoHub-Commander')
    # Для Linux використовуємо ~/.config
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'TamamoHub-Commander')
        
    # Створюємо директорію якщо вона не існує
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_config_path():
    """Отримати шлях до конфігураційного файлу"""
    return os.path.join(get_config_dir(), 'config.json')

def get_log_path():
    """Отримати шлях до файлу логів"""
    return os.path.join(get_config_dir(), 'bot_logs.txt')

def get_templates_path():
    """Отримати шлях до шаблонів"""
    return os.path.join(get_base_path(), 'templates')

def get_static_path():
    """Отримати шлях до статичних файлів"""
    return os.path.join(get_base_path(), 'static') 