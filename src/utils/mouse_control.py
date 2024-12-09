import pyautogui
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..core.logger import log_to_console, log_error

class MouseControl:
    STEP = 20  # Крок переміщення миші в пікселях
    SCROLL_STEP = 10  # Базовий крок прокрутки

    @staticmethod
    def create_mouse_keyboard():
        """Створити клавіатуру керування мишею"""
        try:
            log_to_console("Creating mouse control keyboard")
            keyboard = InlineKeyboardMarkup()
            
            # Кнопки переміщення
            keyboard.row(
                InlineKeyboardButton("↖️", callback_data="mouse:move_up_left"),
                InlineKeyboardButton("⬆️", callback_data="mouse:move_up"),
                InlineKeyboardButton("↗️", callback_data="mouse:move_up_right")
            )
            keyboard.row(
                InlineKeyboardButton("⬅️", callback_data="mouse:move_left"),
                InlineKeyboardButton("•", callback_data="mouse:click"),
                InlineKeyboardButton("➡️", callback_data="mouse:move_right")
            )
            keyboard.row(
                InlineKeyboardButton("↙️", callback_data="mouse:move_down_left"),
                InlineKeyboardButton("⬇️", callback_data="mouse:move_down"),
                InlineKeyboardButton("↘️", callback_data="mouse:move_down_right")
            )
            
            # Кнопки кліків
            keyboard.row(
                InlineKeyboardButton("🖱️ ЛКМ", callback_data="mouse:left_click"),
                InlineKeyboardButton("🖱️ ПКМ", callback_data="mouse:right_click"),
                InlineKeyboardButton("🖱️ 2xЛКМ", callback_data="mouse:double_click")
            )
            
            # Прокрутка
            keyboard.row(
                InlineKeyboardButton("🔄⬆️", callback_data="mouse:scroll_up_fast"),
                InlineKeyboardButton("🔼", callback_data="mouse:scroll_up"),
                InlineKeyboardButton("▲", callback_data="mouse:scroll_up_slow")
            )
            keyboard.row(
                InlineKeyboardButton("🔄⬇️", callback_data="mouse:scroll_down_fast"),
                InlineKeyboardButton("🔽", callback_data="mouse:scroll_down"),
                InlineKeyboardButton("▼", callback_data="mouse:scroll_down_slow")
            )
            
            # Додаткові функції
            keyboard.row(
                InlineKeyboardButton("⚡ Швидкість", callback_data="mouse:speed"),
                InlineKeyboardButton("📍 Центр", callback_data="mouse:center")
            )
            keyboard.row(
                InlineKeyboardButton("🎯 Координати", callback_data="mouse:position")
            )
            
            # Кнопка повернення
            keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
            
            log_to_console("Mouse control keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error("Error creating mouse control keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_speed_keyboard():
        """Створити клавіатуру вибору швидкості"""
        try:
            log_to_console("Creating mouse speed selection keyboard")
            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton("🐌 Повільно", callback_data="mouse:set_speed:10"),
                InlineKeyboardButton("🚶 Середня", callback_data="mouse:set_speed:20"),
                InlineKeyboardButton("🏃 Швидко", callback_data="mouse:set_speed:40")
            )
            keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="mouse:control"))
            log_to_console("Mouse speed keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error("Error creating mouse speed keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def move_mouse(direction):
        """Перемістити мишу"""
        try:
            x, y = 0, 0
            step = MouseControl.STEP
            
            if 'up' in direction:
                y -= step
            if 'down' in direction:
                y += step
            if 'left' in direction:
                x -= step
            if 'right' in direction:
                x += step
                
            current_x, current_y = pyautogui.position()
            log_to_console(f"Moving mouse from ({current_x}, {current_y}) by ({x}, {y})")
            pyautogui.moveRel(x, y)
            new_x, new_y = pyautogui.position()
            log_to_console(f"Mouse moved to new position: ({new_x}, {new_y})")
            return f"Миша переміщена на {x}, {y} пікселів"
        except Exception as e:
            log_error(f"Error moving mouse in direction: {direction}", e)
            return f"Помилка переміщення миші: {str(e)}"

    @staticmethod
    def set_speed(speed):
        """Встановити швидкість миші"""
        try:
            log_to_console(f"Setting mouse speed to: {speed}")
            MouseControl.STEP = speed
            log_to_console(f"Mouse speed set successfully to {speed}")
            return f"Швидкість миші встановлена на {speed} пікселів"
        except Exception as e:
            log_error(f"Error setting mouse speed to {speed}", e)
            return f"Помилка встановлення швидкості: {str(e)}"

    @staticmethod
    def get_position():
        """Отримати поточні координати миші"""
        try:
            x, y = pyautogui.position()
            log_to_console(f"Getting mouse position: ({x}, {y})")
            return f"Поточні координати: X={x}, Y={y}"
        except Exception as e:
            log_error("Error getting mouse position", e)
            return "Помилка отримання координат"

    @staticmethod
    def center_mouse():
        """Перемістити мишу в центр екрану"""
        try:
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            log_to_console(f"Centering mouse to ({center_x}, {center_y})")
            pyautogui.moveTo(center_x, center_y)
            log_to_console("Mouse centered successfully")
            return "Миша переміщена в центр екрану"
        except Exception as e:
            log_error("Error centering mouse", e)
            return "Помилка центрування миші"

    @staticmethod
    def execute_command(command, *args):
        """Виконати команду миші"""
        try:
            log_to_console(f"Executing mouse command: {command}")
            
            if command.startswith("move_"):
                return MouseControl.move_mouse(command.replace("move_", ""))
                
            elif command == "click":
                log_to_console("Performing mouse click")
                pyautogui.click()
                return "Клік"
                
            elif command == "left_click":
                log_to_console("Performing left mouse click")
                pyautogui.click(button='left')
                return "Лівий клік"
                
            elif command == "right_click":
                log_to_console("Performing right mouse click")
                pyautogui.click(button='right')
                return "Правий клік"
                
            elif command == "double_click":
                log_to_console("Performing double click")
                pyautogui.doubleClick()
                return "Подвійний клік"
                
            elif command.startswith("scroll_"):
                direction = "up" if "up" in command else "down"
                speed = "fast" if "fast" in command else "slow" if "slow" in command else "normal"
                multiplier = 3 if speed == "fast" else 0.5 if speed == "slow" else 1
                scroll_amount = MouseControl.SCROLL_STEP * multiplier * (1 if direction == "up" else -1)
                
                log_to_console(f"Scrolling {direction} with speed {speed} (amount: {scroll_amount})")
                pyautogui.scroll(int(scroll_amount))
                return f"{'Швидка' if speed == 'fast' else 'Повільна' if speed == 'slow' else ''} прокрутка {direction}"
                
            elif command == "center":
                return MouseControl.center_mouse()
                
            elif command == "position":
                return MouseControl.get_position()
                
            elif command == "set_speed":
                return MouseControl.set_speed(int(args[0]))
            
            log_to_console(f"Unknown mouse command received: {command}", "WARNING")
            return "Невідома команда"
        except Exception as e:
            log_error(f"Error executing mouse command: {command}", e)
            return f"Помилка виконання команди: {str(e)}" 