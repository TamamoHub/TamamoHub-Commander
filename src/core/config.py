import json
import os
from ..core.logger import log_to_console
from ..core.paths import get_config_path
from ..core.encryption import ConfigEncryption

def load_config():
    try:
        config_path = get_config_path()
        
        if os.path.exists(config_path):
            with open(config_path, 'rb') as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_data = ConfigEncryption.decrypt_data(encrypted_data)
                    if decrypted_data:
                        return json.loads(decrypted_data)
                    else:
                        log_to_console("Помилка розшифрування")
                        
        log_to_console("Створення нової конфігурації")
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
        
        # Конвертуємо в JSON і шифруємо
        json_data = json.dumps(config, indent=4, ensure_ascii=False)
        encrypted_data = ConfigEncryption.encrypt_data(json_data)
        
        if encrypted_data:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'wb') as f:
                f.write(encrypted_data)
                
            log_to_console(f"Конфігурацію збережено в {config_path}")
            return True
        else:
            log_to_console("Помилка шифрування конфігурації")
            return False
            
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