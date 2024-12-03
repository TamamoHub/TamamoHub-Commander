import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class FileExplorer:
    @staticmethod
    def get_drives():
        """Отримати список доступних дисків"""
        return [d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
                if os.path.exists(f"{d}:")]

    @staticmethod
    def get_directory_content(path, page=0, items_per_page=8):
        """Отримати вміст директорії з пагінацією"""
        try:
            items = os.listdir(path)
            # Сортуємо: спочатку папки, потім файли
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            # Пагінація
            total_pages = (len(items) - 1) // items_per_page + 1
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            
            return {
                'items': items[start_idx:end_idx],
                'total_pages': total_pages,
                'current_page': page,
                'has_prev': page > 0,
                'has_next': page < total_pages - 1
            }
        except Exception as e:
            return None

    @staticmethod
    def create_drives_keyboard():
        """Створити клавіатуру з дисками"""
        keyboard = InlineKeyboardMarkup()
        drives = FileExplorer.get_drives()
        
        # Додаємо кнопки для кожного диску по 2 в ряд
        for i in range(0, len(drives), 2):
            row = []
            for drive in drives[i:i+2]:
                row.append(InlineKeyboardButton(
                    f"💿 {drive}:", 
                    callback_data=f"explorer:drive:{drive}:"
                ))
            keyboard.row(*row)
        
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
        return keyboard

    @staticmethod
    def create_folder_keyboard(path, page=0):
        """Створити клавіатуру для папки"""
        keyboard = InlineKeyboardMarkup()
        content = FileExplorer.get_directory_content(path, page)
        
        if content is None:
            keyboard.row(InlineKeyboardButton(
                "⚠️ Помилка доступу", 
                callback_data="explorer:drives"
            ))
            return keyboard
        
        # Додаємо елементи
        for item in content['items']:
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            icon = "📁" if is_dir else "📄"
            
            if is_dir:
                callback_data = f"explorer:folder:{full_path}"
            else:
                callback_data = f"explorer:file:{full_path}"
            
            keyboard.row(InlineKeyboardButton(
                f"{icon} {item}", 
                callback_data=callback_data
            ))
        
        # Навігаційні кнопки
        nav_buttons = []
        if content['has_prev']:
            nav_buttons.append(InlineKeyboardButton(
                "⬅️", callback_data=f"explorer:page:{path}:{page-1}"
            ))
        if content['has_next']:
            nav_buttons.append(InlineKeyboardButton(
                "➡️", callback_data=f"explorer:page:{path}:{page+1}"
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
        
        # Кнопки навігації
        bottom_buttons = []
        if os.path.dirname(path) != path:
            bottom_buttons.append(InlineKeyboardButton(
                "⬅️ Назад", 
                callback_data=f"explorer:folder:{os.path.dirname(path)}"
            ))
        bottom_buttons.append(InlineKeyboardButton(
            "💿 До дисків", 
            callback_data="explorer:drives"
        ))
        keyboard.row(*bottom_buttons)
        
        return keyboard

    @staticmethod
    def create_file_keyboard(file_path):
        """Створити клавіатуру для файлу"""
        keyboard = InlineKeyboardMarkup()
        
        # Кнопки дій
        keyboard.row(
            InlineKeyboardButton(
                "▶️ Запустити", 
                callback_data=f"file:run:{file_path}"
            ),
            InlineKeyboardButton(
                "⬇️ Завантажити", 
                callback_data=f"file:download:{file_path}"
            )
        )
        keyboard.row(InlineKeyboardButton(
            "🗑️ Видалити", 
            callback_data=f"file:delete:{file_path}"
        ))
        
        # Навігація
        keyboard.row(
            InlineKeyboardButton(
                "⬅️ Назад", 
                callback_data=f"explorer:folder:{os.path.dirname(file_path)}"
            ),
            InlineKeyboardButton(
                "💿 До дисків", 
                callback_data="explorer:drives"
            )
        )
        
        return keyboard

    @staticmethod
    def create_delete_confirmation_keyboard(file_path):
        """Створити клавіатуру підтвердження видалення"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(
                "✅ Так", 
                callback_data=f"file:confirm_delete:{file_path}"
            ),
            InlineKeyboardButton(
                "❌ Ні", 
                callback_data=f"explorer:file:{file_path}"
            )
        )
        return keyboard

    @staticmethod
    def run_file(file_path):
        """Запустити файл"""
        try:
            os.startfile(file_path)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_file(file_path):
        """Видалити файл"""
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False 