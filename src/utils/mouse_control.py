import pyautogui
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class MouseControl:
    STEP = 20  # Крок переміщення миші в пікселях
    SCROLL_STEP = 10  # Базовий крок прокрутки

    @staticmethod
    def create_mouse_keyboard():
        """Створити клавіатуру керування мишею"""
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
        
        return keyboard

    @staticmethod
    def create_speed_keyboard():
        """Створити клавіатуру вибору швидкості"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("🐌 Повільно", callback_data="mouse:set_speed:10"),
            InlineKeyboardButton("🚶 Середня", callback_data="mouse:set_speed:20"),
            InlineKeyboardButton("🏃 Швидко", callback_data="mouse:set_speed:40")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="mouse:control"))
        return keyboard

    @staticmethod
    def move_mouse(direction):
        """Перемістити мишу"""
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
        pyautogui.moveRel(x, y)
        return f"Миша переміщена на {x}, {y} пікселів"

    @staticmethod
    def set_speed(speed):
        """Встановити швидкість миші"""
        MouseControl.STEP = speed
        return f"Швидкість миші встановлена на {speed} пікселів"

    @staticmethod
    def get_position():
        """Отримати поточні координати миші"""
        x, y = pyautogui.position()
        return f"Поточні координати: X={x}, Y={y}"

    @staticmethod
    def center_mouse():
        """Перемістити мишу в центр екрану"""
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)
        return "Миша переміщена в центр екрану"

    @staticmethod
    def execute_command(command, *args):
        """Виконати команду миші"""
        try:
            if command.startswith("move_"):
                return MouseControl.move_mouse(command.replace("move_", ""))
                
            elif command == "click":
                pyautogui.click()
                return "Клік"
                
            elif command == "left_click":
                pyautogui.click(button='left')
                return "Лівий клік"
                
            elif command == "right_click":
                pyautogui.click(button='right')
                return "Правий клік"
                
            elif command == "double_click":
                pyautogui.doubleClick()
                return "Подвійний клік"
                
            elif command == "scroll_up":
                pyautogui.scroll(MouseControl.SCROLL_STEP)
                return "Прокрутка вгору"
                
            elif command == "scroll_down":
                pyautogui.scroll(-MouseControl.SCROLL_STEP)
                return "Прокрутка вниз"
                
            elif command == "scroll_up_fast":
                pyautogui.scroll(MouseControl.SCROLL_STEP * 3)
                return "Швидка прокрутка вгору"
                
            elif command == "scroll_down_fast":
                pyautogui.scroll(-MouseControl.SCROLL_STEP * 3)
                return "Швидка прокрутка вниз"
                
            elif command == "scroll_up_slow":
                pyautogui.scroll(MouseControl.SCROLL_STEP // 2)
                return "Повільна прокрутка вгору"
                
            elif command == "scroll_down_slow":
                pyautogui.scroll(-MouseControl.SCROLL_STEP // 2)
                return "Повільна прокрутка вниз"
                
            elif command == "center":
                return MouseControl.center_mouse()
                
            elif command == "position":
                return MouseControl.get_position()
                
            elif command == "set_speed":
                return MouseControl.set_speed(int(args[0]))
            
            return "Невідома команда"
        except Exception as e:
            return f"Помилка виконання команди: {str(e)}" 