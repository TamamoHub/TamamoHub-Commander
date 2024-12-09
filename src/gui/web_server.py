from flask import Flask, render_template, jsonify, request
from flask_sock import Sock
from ..core.config import load_config, save_config
from ..bot.bot_manager import get_bot_status, start_bot as start_telegram_bot, stop_bot
from src.utils.updater import check_updates, update_app
from ..utils.statistics import stats
from ..core.paths import get_config_path
from ..core.logger import logger
import os
import threading
import time

app = Flask(__name__, 
           template_folder='../../templates',
           static_folder='../../static')
sock = Sock(app)

# Флаг для контролю роботи WebSocket
ws_running = True

@sock.route('/ws')
def websocket(ws):
    """WebSocket з'єднання для консолі"""
    global ws_running
    try:
        # Додаємо клієнта до списку
        logger.websocket_clients.add(ws)
        
        # Відправляємо всі існуючі логи
        logs = logger.get_logs()
        if logs:
            ws.send(logs)
            
        # Чекаємо на закриття з'єднання
        while ws_running:
            try:
                # Отримуємо повідомлення з таймаутом
                message = ws.receive(timeout=1.0)
                if message is None:
                    continue
            except Exception:
                # Перевіряємо чи з'єднання ще активне
                try:
                    ws.send("ping")
                except:
                    break
            time.sleep(0.1)  # Зменшуємо навантаження на CPU
                
    finally:
        # Видаляємо клієнта при закритті з'єднання
        if ws in logger.websocket_clients:
            logger.websocket_clients.remove(ws)

def shutdown_server():
    """Коректне завершення роботи сервера"""
    global ws_running
    ws_running = False
    # Закриваємо всі WebSocket з'єднання
    for ws in logger.websocket_clients.copy():
        try:
            ws.close()
        except:
            pass
    logger.websocket_clients.clear()

@app.route('/shutdown')
def shutdown():
    """Endpoint для завершення роботи сервера"""
    shutdown_server()
    return jsonify({"status": "success"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_settings')
def load_settings():
    config = load_config()
    return jsonify(config)

@app.route('/save_settings', methods=['POST'])
def save_settings():
    try:
        config = request.get_json()
        if config is None:
            return jsonify({"status": "error", "message": "Invalid JSON data"})
            
        current_config = load_config()
        if 'admin_id' in current_config:
            config['admin_id'] = current_config['admin_id']
            
        success = save_config(config)
        if success:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Failed to save config"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/bot_status')
def bot_status():
    status = get_bot_status()
    return jsonify(status)

@app.route('/start_bot')
def start_bot_route():
    try:
        config = load_config()
        if config['telegram_token']:
            success = start_telegram_bot(config['telegram_token'])
            if success:
                return jsonify({"status": "success"})
            return jsonify({"status": "error", "message": "Failed to start bot"})
        return jsonify({"status": "error", "message": "Token not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop_bot')
def stop_bot_route():
    try:
        success = stop_bot()
        if success:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Failed to stop bot"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/check_updates')
def check_for_updates():
    """Перевірка наявності оновлень"""
    update_info = check_updates()
    return jsonify(update_info)

@app.route('/update_app')
def update_application():
    """Оновити програму"""
    result = update_app()
    return jsonify(result)

@app.route('/get_statistics')
def get_statistics():
    return jsonify(stats.get_statistics())

@app.route('/config_path')
def get_config_location():
    return jsonify({"path": get_config_path()})

@app.route('/reset_settings')
def reset_settings():
    try:
        config_path = get_config_path()
        if os.path.exists(config_path):
            os.remove(config_path)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route('/get_logs')
def get_logs():
    """Endpoint для отримання всіх логів"""
    from ..core.logger import get_logs
    return get_logs()