import json
import os
from ..core.logger import log_to_console
import sys

def get_config_path():
    """Отримати шлях до конфігураційного файлу"""
    if getattr(sys, 'frozen', False):
        # Якщо запущено як exe
        base_path = sys._MEIPASS
    else:
        # Якщо запущено як python скрипт
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, 'config.json')

def load_config():
    try:
        config_path = get_config_path()
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        log_to_console(f"Конфігураційний файл не знайдено, створюємо новий")
    except Exception as e:
        log_to_console(f"Помилка завантаження конфігурації: {str(e)}")
    
    # Повертаємо конфігурацію за замовчуванням
    return {
        'telegram_token': '',
        'ai_model': 'gemini',
        'ai_token': '',
        'admin_id': None
    }

def save_config(config):
    try:
        config_path = get_config_path()
        
        # Зберігаємо з форматуванням
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            
        log_to_console(f"Конфігурацію успішно збережено в {config_path}")
        return True
    except Exception as e:
        log_to_console(f"Помилка збереження конфігурації: {str(e)}")
        return False

def get_admin_id():
    config = load_config()
    return config.get('admin_id', None)

def set_admin_id(admin_id):
    config = load_config()
    config['admin_id'] = admin_id
    save_config(config) 