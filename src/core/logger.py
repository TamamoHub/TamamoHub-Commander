import queue
import os
from datetime import datetime

message_queue = queue.Queue()
websocket_clients = set()
LOG_FILE = "bot_logs.txt"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB

def log_to_console(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    
    # Виводимо в консоль
    print(formatted_message)
    
    # Зберігаємо в файл
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(formatted_message + '\n')
    
    # Відправляємо в чергу для веб-інтерфейсу
    message_queue.put(formatted_message)
    
    # Відправляємо клієнтам WebSocket
    websocket_clients_copy = websocket_clients.copy()
    for client in websocket_clients_copy:
        try:
            client.send(formatted_message)
        except Exception as e:
            print(f"Помилка відправки до клієнта: {e}")
            if client in websocket_clients:
                websocket_clients.remove(client)
    
    # Перевіряємо розмір файлу
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
            # Створюємо архівний файл
            archive_name = f"bot_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            os.rename(LOG_FILE, archive_name)
    except Exception as e:
        print(f"Помилка ротації логів: {e}")

def get_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception as e:
        print(f"Помилка читання логів: {e}")
        return ""

def clear_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write("")
    except Exception as e:
        print(f"Помилка очищення логів: {e}")