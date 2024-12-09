import os
import subprocess
import pyautogui
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..core.logger import log_to_console, log_error

class WindowsCommands:
    @staticmethod
    def create_commands_keyboard():
        """Створити клавіатуру з командами Windows"""
        try:
            log_to_console("Creating Windows commands keyboard")
            keyboard = InlineKeyboardMarkup(row_width=2)
            
            # Системні команди
            keyboard.add(
                InlineKeyboardButton("🔌 Вимкнути ПК", callback_data="wincmd:shutdown"),
                InlineKeyboardButton("🔄 Перезавантажити", callback_data="wincmd:reboot")
            )
            keyboard.add(
                InlineKeyboardButton("🛑 Відмінити вимкнення", callback_data="wincmd:abort_shutdown"),
                InlineKeyboardButton("🔒 Заблокувати", callback_data="wincmd:lock")
            )
            keyboard.add(
                InlineKeyboardButton("😴 Сплячий режим", callback_data="wincmd:sleep"),
                InlineKeyboardButton("🗑️ Очистити корзину", callback_data="wincmd:clear_bin")
            )
            
            # Вікна та інтерфейс
            keyboard.add(
                InlineKeyboardButton("⬇️ Згорнути все", callback_data="wincmd:minimize_all"),
                InlineKeyboardButton("↙️ Згорнути поточне", callback_data="wincmd:minimize_current")
            )
            keyboard.add(
                InlineKeyboardButton("↗️ На весь екран", callback_data="wincmd:maximize"),
                InlineKeyboardButton("📸 Скріншот", callback_data="wincmd:screenshot")
            )
            
            # Системні утиліти
            keyboard.add(
                InlineKeyboardButton("⚙️ Налаштування", callback_data="wincmd:settings"),
                InlineKeyboardButton("❌ Закрити налаштування", callback_data="wincmd:close_settings")
            )
            keyboard.add(
                InlineKeyboardButton("📋 Буфер обміну", callback_data="wincmd:clipboard"),
                InlineKeyboardButton("📊 Диспетчер задач", callback_data="wincmd:task_manager")
            )
            keyboard.add(
                InlineKeyboardButton("⬇️ Завантаження", callback_data="wincmd:downloads"),
                InlineKeyboardButton("🌐 Змінити мову", callback_data="wincmd:language")
            )

            # Кнопка повернення
            keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
            
            log_to_console("Windows commands keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error("Error creating Windows commands keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def execute_command(command):
        """Виконати Windows команду"""
        try:
            log_to_console(f"Executing Windows command: {command}")
            
            if command == "shutdown":
                log_to_console("Initiating system shutdown")
                os.system("shutdown /s /t 10")
                return "ПК буде вимкнено через 10 секунд"
            
            elif command == "reboot":
                log_to_console("Initiating system reboot")
                os.system("shutdown /r /t 10")
                return "ПК буде перезавантажено через 10 секунд"
            
            elif command == "abort_shutdown":
                log_to_console("Aborting system shutdown")
                os.system("shutdown /a")
                return "Вимкнення скасовано"
            
            elif command == "lock":
                log_to_console("Locking workstation")
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "ПК заблоковано"
            
            elif command == "sleep":
                log_to_console("Putting system to sleep")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "ПК переведено в сплячий режим"
            
            elif command == "clear_bin":
                log_to_console("Clearing recycle bin")
                os.system("rd /s /q %systemdrive%\$Recycle.bin")
                return "Корзину очищено"
            
            elif command == "minimize_all":
                log_to_console("Minimizing all windows")
                pyautogui.hotkey('win', 'd')
                return "Всі вікна згорнуто"
            
            elif command == "minimize_current":
                log_to_console("Minimizing current window")
                pyautogui.hotkey('win', 'down')
                return "Поточне вікно згорнуто"
            
            elif command == "maximize":
                log_to_console("Maximizing current window")
                pyautogui.hotkey('win', 'up')
                return "Поточне вікно розгорнуто"
            
            elif command == "screenshot":
                log_to_console("Taking screenshot")
                screenshot = pyautogui.screenshot()
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot.save(filename)
                log_to_console(f"Screenshot saved as: {filename}")
                return filename
            
            elif command == "settings":
                log_to_console("Opening Windows settings")
                os.system("start ms-settings:")
                return "Відкрито налаштування Windows"
            
            elif command == "close_settings":
                log_to_console("Closing Windows settings")
                os.system("taskkill /f /im SystemSettings.exe")
                return "Налаштування закрито"
            
            elif command == "clipboard":
                log_to_console("Opening clipboard history")
                pyautogui.hotkey('win', 'v')
                return "Відкрито буфер обміну"
            
            elif command == "task_manager":
                log_to_console("Opening task manager")
                os.system("taskmgr")
                return "Відкрито диспетчер задач"
            
            elif command == "downloads":
                log_to_console("Opening downloads folder")
                os.startfile(os.path.expanduser("~\\Downloads"))
                return "Відкрито папку завантажень"
            
            elif command == "language":
                log_to_console("Opening language switcher")
                pyautogui.hotkey('win', 'space')
                return "Відкрито меню зміни мови"
            
            log_to_console("Command executed successfully")
            return "Команду виконано"
        except Exception as e:
            log_error(f"Error executing Windows command: {command}", e)
            return f"Помилка виконання команди: {str(e)}" 