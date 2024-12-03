from flask import Flask, render_template, jsonify, request
from ..core.config import load_config, save_config
from ..bot.bot_manager import get_bot_status

app = Flask(__name__, 
           template_folder='../../templates',
           static_folder='../../static')

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
def start_bot():
    try:
        config = load_config()
        if config['telegram_token']:
            from ..bot.bot_manager import start_bot
            start_bot(config['telegram_token'])
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Token not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop_bot')
def stop_bot():
    try:
        from ..bot.bot_manager import stop_bot
        stop_bot()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})