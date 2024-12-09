import telebot
from threading import Thread
from ..core.config import load_config
from ..core.logger import log_to_console
from .handlers import setup_handlers
from ..utils.statistics import stats

bot = None
bot_thread = None

def handle_message(message):
    """Обробник всіх повідомлень"""
    stats.add_message(message.from_user.id)
    # інша логіка обробки повідомлень...

def handle_start(message):
    """Обробник команди /start"""
    stats.add_command('start')
    # інша логіка команди...

def handle_help(message):
    """Обробник команди /help"""
    stats.add_command('help')
    # інша логіка команди...

def setup_message_handlers(bot_instance):
    """Налаштування обробників повідомлень"""
    bot_instance.message_handler(func=lambda message: True)(handle_message)
    bot_instance.message_handler(commands=['start'])(handle_start)
    bot_instance.message_handler(commands=['help'])(handle_help)

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
        # Спочатку зупиняємо існуючого бота
        stop_bot()
        
        # Створюємо нового бота
        bot = telebot.TeleBot(token)
        setup_handlers(bot)
        setup_message_handlers(bot)
            
        # Запускаємо в новому потоці
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
            # Чекаємо завершення потоку з таймаутом
            if bot_thread and bot_thread.is_alive():
                bot_thread.join(timeout=2.0)
                # Якщо потік все ще живий, форсуємо завершення
                if bot_thread.is_alive():
                    log_to_console("Форсоване завершення потоку бота", "WARNING")
            bot = None
            bot_thread = None
            
        log_to_console("Бот зупинений!")
        return True
        
    except Exception as e:
        log_to_console(f"Помилка зупинки бота: {str(e)}")
        return False

def get_bot():
    """Отримати екземпляр бота"""
    return bot