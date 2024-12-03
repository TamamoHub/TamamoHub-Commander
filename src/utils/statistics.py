from datetime import datetime
from ..bot.bot_manager import bot_instance

def get_statistics():
    # Тут можна додати реальний збір статистики
    return {
        'total_messages': 0,
        'active_users': 0,
        'uptime': '0:00:00',
        'commands_used': {
            'start': 0,
            'help': 0
        }
    } 