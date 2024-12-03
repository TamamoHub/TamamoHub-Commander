import psutil
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class TaskManager:
    @staticmethod
    def get_running_processes(page=0, per_page=15):
        """Отримати список запущених процесів"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'exe']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'status': proc.info['status'],
                    'exe': proc.info['exe']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Сортуємо за іменем
        processes.sort(key=lambda x: x['name'].lower())
        
        # Пагінація
        total_pages = (len(processes) - 1) // per_page + 1
        start_idx = page * per_page
        end_idx = start_idx + per_page
        
        return {
            'processes': processes[start_idx:end_idx],
            'total_pages': total_pages,
            'current_page': page,
            'has_prev': page > 0,
            'has_next': page < total_pages - 1
        }

    @staticmethod
    def kill_process(pid):
        """Завершити процес"""
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except:
            return False

    @staticmethod
    def restart_process(pid):
        """Перезапустити процес"""
        try:
            process = psutil.Process(pid)
            exe_path = process.exe()
            name = process.name()
            
            # Спочатку завершуємо процес
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
            
            # Запускаємо новий процес
            import subprocess
            if exe_path:
                subprocess.Popen([exe_path])
            else:
                subprocess.Popen([name])
            return True
        except Exception as e:
            print(f"Помилка перезапуску процесу: {e}")
            return False

    @staticmethod
    def start_process(name):
        """Запустити новий процес"""
        try:
            import subprocess
            subprocess.Popen(name)
            return True
        except:
            return False

    @staticmethod
    def create_task_manager_keyboard():
        """Створити головну клавіатуру диспетчера завдань"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("▶️ Запустити новий процес", callback_data="taskman:new"),
            InlineKeyboardButton(" Керувати запущеними", callback_data="taskman:list:0")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
        return keyboard

    @staticmethod
    def create_process_list_keyboard(page=0):
        """Створити клавіатуру зі списком процесів"""
        keyboard = InlineKeyboardMarkup()
        processes = TaskManager.get_running_processes(page)
        
        for proc in processes['processes']:
            status_icon = "🟢" if proc['status'] == "running" else "🔴"
            keyboard.row(InlineKeyboardButton(
                f"{status_icon} {proc['name']} (PID: {proc['pid']})",
                callback_data=f"taskman:process:{proc['pid']}"
            ))
        
        # Додаємо номер сторінки
        nav_text = f"Сторінка {page + 1} з {processes['total_pages']}"
        keyboard.row(InlineKeyboardButton(nav_text, callback_data="ignore"))
        
        # Навігаційні кнопки
        nav_buttons = []
        if processes['has_prev']:
            nav_buttons.append(InlineKeyboardButton(
                "⬅️", callback_data=f"taskman:list:{page-1}"
            ))
        if processes['has_next']:
            nav_buttons.append(InlineKeyboardButton(
                "➡️", callback_data=f"taskman:list:{page+1}"
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
        
        # Кнопка повернення
        keyboard.row(InlineKeyboardButton(
            "⬅️ Назад",
            callback_data="taskman:main"
        ))
        
        return keyboard

    @staticmethod
    def create_process_control_keyboard(pid):
        """Створити клавіатуру керування процесом"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(
                "🔄 Перезапустити",
                callback_data=f"taskman:restart:{pid}"
            ),
            InlineKeyboardButton(
                "❌ Завершити",
                callback_data=f"taskman:kill:{pid}"
            )
        )
        keyboard.row(InlineKeyboardButton(
            "⬅️ Назад",
            callback_data="taskman:list:0"
        ))
        return keyboard 