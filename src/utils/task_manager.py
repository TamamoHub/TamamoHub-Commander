import psutil
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, List, Optional
from ..core.logger import log_to_console, log_error

class TaskManager:
    @staticmethod
    def get_running_processes(page: int = 0, per_page: int = 15) -> Dict:
        """Отримати список запущених процесів"""
        try:
            log_to_console(f"Getting running processes (page {page}, per_page {per_page})")
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'exe', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': proc.info['status'],
                        'exe': proc.info['exe'],
                        'cpu': proc.info.get('cpu_percent', 0),
                        'memory': proc.info.get('memory_percent', 0)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    log_error(f"Error getting process info: PID {proc.info.get('pid', 'unknown')}", e)
                    continue
            
            # Сортуємо за іменем
            processes.sort(key=lambda x: x['name'].lower())
            
            # Пагінація
            total_pages = (len(processes) - 1) // per_page + 1
            start_idx = page * per_page
            end_idx = start_idx + per_page
            
            log_to_console(f"Found {len(processes)} processes, showing page {page+1} of {total_pages}")
            return {
                'processes': processes[start_idx:end_idx],
                'total_pages': total_pages,
                'current_page': page,
                'has_prev': page > 0,
                'has_next': page < total_pages - 1
            }
        except Exception as e:
            log_error("Error getting running processes", e)
            return {
                'processes': [],
                'total_pages': 1,
                'current_page': 0,
                'has_prev': False,
                'has_next': False
            }

    @staticmethod
    def kill_process(pid):
        """Завершити процес"""
        try:
            log_to_console(f"Attempting to kill process with PID: {pid}")
            process = psutil.Process(pid)
            process_name = process.name()
            process.kill()
            log_to_console(f"Successfully killed process {process_name} (PID: {pid})")
            return True
        except Exception as e:
            log_error(f"Error killing process with PID {pid}", e)
            return False

    @staticmethod
    def restart_process(pid: int) -> bool:
        """Перезапустити процес"""
        try:
            log_to_console(f"Attempting to restart process with PID: {pid}")
            process = psutil.Process(pid)
            exe_path = process.exe()
            name = process.name()
            cmd_line = process.cmdline()
            
            log_to_console(f"Terminating process {name} (PID: {pid})")
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                log_to_console(f"Process {pid} termination timeout, forcing kill")
                process.kill()
                process.wait(timeout=3)
            
            import subprocess
            log_to_console(f"Restarting process {name}")
            if cmd_line:
                subprocess.Popen(cmd_line)
                log_to_console(f"Process restarted with command line: {' '.join(cmd_line)}")
            elif exe_path:
                subprocess.Popen([exe_path])
                log_to_console(f"Process restarted with exe path: {exe_path}")
            else:
                subprocess.Popen([name])
                log_to_console(f"Process restarted with name: {name}")
            return True
        except Exception as e:
            log_error(f"Error restarting process with PID {pid}", e)
            return False

    @staticmethod
    def start_process(name):
        """Запустити новий процес"""
        try:
            log_to_console(f"Attempting to start new process: {name}")
            import subprocess
            subprocess.Popen(name)
            log_to_console(f"Successfully started process: {name}")
            return True
        except Exception as e:
            log_error(f"Error starting process: {name}", e)
            return False

    @staticmethod
    def create_task_manager_keyboard():
        """Створити головну клавіатуру диспетчера завдань"""
        try:
            log_to_console("Creating task manager main keyboard")
            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton("▶️ Запустити новий процес", callback_data="taskman:new"),
                InlineKeyboardButton(" Керувати запущеними", callback_data="taskman:list:0")
            )
            keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
            log_to_console("Task manager keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error("Error creating task manager keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_process_list_keyboard(page: int = 0) -> InlineKeyboardMarkup:
        """Створити клавіатуру зі списком процесів"""
        try:
            log_to_console(f"Creating process list keyboard for page {page}")
            keyboard = InlineKeyboardMarkup()
            processes = TaskManager.get_running_processes(page)
            
            for proc in processes['processes']:
                status_icon = "🟢" if proc['status'] == "running" else "🔴"
                process_info = f"{status_icon} {proc['name']} (PID: {proc['pid']}) CPU: {proc['cpu']:.1f}% MEM: {proc['memory']:.1f}%"
                keyboard.row(InlineKeyboardButton(
                    process_info,
                    callback_data=f"taskman:process:{proc['pid']}"
                ))
            
            # Додаємо навігаційні елементи...
            log_to_console(f"Process list keyboard created with {len(processes['processes'])} processes")
            return keyboard
        except Exception as e:
            log_error("Error creating process list keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_process_control_keyboard(pid):
        """Створити клавіатуру керування процесом"""
        try:
            log_to_console(f"Creating control keyboard for process PID: {pid}")
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
            log_to_console(f"Control keyboard created for PID: {pid}")
            return keyboard
        except Exception as e:
            log_error(f"Error creating process control keyboard for PID {pid}", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def get_process_details(pid: int) -> Optional[Dict]:
        """Отримати детальну інформацію про процес"""
        try:
            log_to_console(f"Getting details for process PID: {pid}")
            process = psutil.Process(pid)
            details = {
                'pid': process.pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'create_time': process.create_time(),
                'exe': process.exe(),
                'cmdline': process.cmdline(),
                'username': process.username()
            }
            log_to_console(f"Successfully retrieved details for process {details['name']} (PID: {pid})")
            return details
        except Exception as e:
            log_error(f"Error getting process details for PID {pid}", e)
            return None