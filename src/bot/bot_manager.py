import telebot
from threading import Thread
from ..core.config import load_config
from ..core.logger import log_to_console
from .handlers import setup_handlers

bot = None
bot_thread = None

def get_bot_status():
    """Отримати статус бота"""
    return {
        'is_active': bot is not None and bot_thread is not None and bot_thread.is_alive(),
        'thread_status': 'Running' if bot_thread and bot_thread.is_alive() else 'Stopped'
    }

def start_bot(token):
    """Запустити бота"""
    global bot, bot_thread
    
    try:
        if bot is None:
            bot = telebot.TeleBot(token)
            setup_handlers(bot)
            
        if bot_thread is None or not bot_thread.is_alive():
            bot_thread = Thread(target=bot.polling, args=(True,))
            bot_thread.daemon = True
            bot_thread.start()
            log_to_console("Бот успішно запущений!")
            return True
            
    except Exception as e:
        log_to_console(f"Помилка запуску бота: {str(e)}")
        return False

def stop_bot():
    """Зупинити бота"""
    global bot, bot_thread
    
    try:
        if bot:
            bot.stop_polling()
            bot = None
            
        if bot_thread:
            bot_thread = None
            
        log_to_console("Бот зупинений!")
        return True
        
    except Exception as e:
        log_to_console(f"Помилка зупинки бота: {str(e)}")
        return False

def get_bot():
    """Отримати екземпляр бота"""
    return bot 