from datetime import datetime
from collections import defaultdict, Counter

class Statistics:
    def __init__(self):
        self.start_time = datetime.now()
        self.total_messages = 0
        self.active_users = set()
        self.commands_used = defaultdict(int)
        self.hourly_activity = defaultdict(int)  # Активність по годинах
        self.daily_stats = defaultdict(int)      # Статистика по днях
        self.user_activity = defaultdict(int)    # Активність користувачів
        self.message_types = Counter()           # Типи повідомлень
        self.peak_online = 0                     # Пік онлайн користувачів
        self.total_media = 0                     # Загальна кількість медіа
        self.errors_count = 0                    # Кількість помилок
        self.successful_responses = 0            # Успішні відповіді
        
    def add_message(self, user_id, message_type="text"):
        self.total_messages += 1
        self.active_users.add(user_id)
        self.user_activity[user_id] += 1
        self.message_types[message_type] += 1
        
        # Оновлюємо погодинну статистику
        hour = datetime.now().hour
        self.hourly_activity[hour] += 1
        
        # Оновлюємо денну статистику
        day = datetime.now().strftime("%Y-%m-%d")
        self.daily_stats[day] += 1
        
        # Оновлюємо пік онлайн
        current_online = len(self.active_users)
        if current_online > self.peak_online:
            self.peak_online = current_online
            
    def add_media(self):
        self.total_media += 1
        
    def add_error(self):
        self.errors_count += 1
        
    def add_success(self):
        self.successful_responses += 1

    def get_uptime(self):
        delta = datetime.now() - self.start_time
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = delta.seconds % 60
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def get_statistics(self):
        success_rate = (self.successful_responses / (self.successful_responses + self.errors_count) * 100) if (self.successful_responses + self.errors_count) > 0 else 0
        
        return {
            'general': {
                'total_messages': self.total_messages,
                'active_users': len(self.active_users),
                'uptime': self.get_uptime(),
                'peak_online': self.peak_online,
                'success_rate': f"{success_rate:.1f}%"
            },
            'activity': {
                'hourly': dict(self.hourly_activity),
                'daily': dict(self.daily_stats),
                'message_types': dict(self.message_types)
            },
            'users': {
                'most_active': dict(sorted(self.user_activity.items(), key=lambda x: x[1], reverse=True)[:5]),
                'total_users': len(self.active_users)
            },
            'performance': {
                'errors': self.errors_count,
                'successful': self.successful_responses,
                'media_processed': self.total_media
            },
            'commands': dict(self.commands_used)
        }

stats = Statistics() 