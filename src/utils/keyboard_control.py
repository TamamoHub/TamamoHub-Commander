import pyautogui
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class KeyboardControl:
    @staticmethod
    def create_keyboard_menu():
        """Створити головне меню клавіатури"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("⌨️ Функціональні клавіші", callback_data="keyboard:function_keys"),
            InlineKeyboardButton(" Ввести текст", callback_data="keyboard:input_text")
        )
        keyboard.row(
            InlineKeyboardButton("🎮 Гарячі клавіші", callback_data="keyboard:hotkeys"),
            InlineKeyboardButton("⚡ Спеціальні", callback_data="keyboard:special")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
        return keyboard

    @staticmethod
    def create_function_keys_keyboard():
        """Створити клавіатуру функціональних клавіш"""
        keyboard = InlineKeyboardMarkup()
        # F1-F12
        for i in range(1, 13, 3):
            keyboard.row(
                *[InlineKeyboardButton(f"F{j}", callback_data=f"keyboard:press:f{j}") 
                  for j in range(i, min(i+3, 13))]
            )
        # Навігаційні клавіші
        keyboard.row(
            InlineKeyboardButton("Home", callback_data="keyboard:press:home"),
            InlineKeyboardButton("End", callback_data="keyboard:press:end"),
            InlineKeyboardButton("PgUp", callback_data="keyboard:press:pageup")
        )
        keyboard.row(
            InlineKeyboardButton("Insert", callback_data="keyboard:press:insert"),
            InlineKeyboardButton("Delete", callback_data="keyboard:press:delete"),
            InlineKeyboardButton("PgDn", callback_data="keyboard:press:pagedown")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="keyboard:menu"))
        return keyboard

    @staticmethod
    def create_hotkeys_keyboard():
        """Створити клавіатуру гарячих клавіш"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("📋 Copy", callback_data="keyboard:hotkey:ctrl+c"),
            InlineKeyboardButton("📋 Paste", callback_data="keyboard:hotkey:ctrl+v"),
            InlineKeyboardButton("✂️ Cut", callback_data="keyboard:hotkey:ctrl+x")
        )
        keyboard.row(
            InlineKeyboardButton("↩️ Undo", callback_data="keyboard:hotkey:ctrl+z"),
            InlineKeyboardButton("↪️ Redo", callback_data="keyboard:hotkey:ctrl+y"),
            InlineKeyboardButton("💾 Save", callback_data="keyboard:hotkey:ctrl+s")
        )
        keyboard.row(
            InlineKeyboardButton("🔍 Find", callback_data="keyboard:hotkey:ctrl+f"),
            InlineKeyboardButton("📝 Select All", callback_data="keyboard:hotkey:ctrl+a"),
            InlineKeyboardButton("🖨️ Print", callback_data="keyboard:hotkey:ctrl+p")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="keyboard:menu"))
        return keyboard

    @staticmethod
    def create_special_keyboard():
        """Створити клавіатуру спеціальних клавіш"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("⏎ Enter", callback_data="keyboard:press:enter"),
            InlineKeyboardButton("⌫ Backspace", callback_data="keyboard:press:backspace"),
            InlineKeyboardButton("⎵ Space", callback_data="keyboard:press:space")
        )
        keyboard.row(
            InlineKeyboardButton("⇥ Tab", callback_data="keyboard:press:tab"),
            InlineKeyboardButton("⎋ Esc", callback_data="keyboard:press:esc"),
            InlineKeyboardButton("⇪ Caps", callback_data="keyboard:press:capslock")
        )
        keyboard.row(
            InlineKeyboardButton("Alt", callback_data="keyboard:press:alt"),
            InlineKeyboardButton("Ctrl", callback_data="keyboard:press:ctrl"),
            InlineKeyboardButton("Shift", callback_data="keyboard:press:shift")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="keyboard:menu"))
        return keyboard

    @staticmethod
    def execute_command(command, *args):
        """Виконати команду клавіатури"""
        try:
            if command == "press":
                key = args[0]
                pyautogui.press(key)
                return f"Натиснуто клавішу {key.upper()}"
                
            elif command == "hotkey":
                keys = args[0].split('+')
                pyautogui.hotkey(*keys)
                return f"Виконано комбінацію {'+'.join(keys).upper()}"
                
            elif command == "type":
                text = args[0]
                pyautogui.write(text)
                return f"Введено текст: {text}"
            
            return "Невідома команда"
        except Exception as e:
            return f"Помилка виконання команди: {str(e)}" 