import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..core.logger import log_to_console, log_error

class FileExplorer:
    @staticmethod
    def get_drives():
        """Отримати список доступних дисків"""
        try:
            log_to_console("Scanning for available drives...")
            drives = [d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
                    if os.path.exists(f"{d}:")]
            log_to_console(f"Found drives: {', '.join(drives)}")
            return drives
        except Exception as e:
            log_error("Error scanning drives", e)
            return []

    @staticmethod
    def get_directory_content(path, page=0, items_per_page=8):
        """Отримати вміст директорії з пагінацією"""
        try:
            log_to_console(f"Reading directory content: {path} (page {page})")
            items = os.listdir(path)
            # Сортуємо: спочатку папки, потім файли
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            # Пагінація
            total_pages = (len(items) - 1) // items_per_page + 1
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            
            result = {
                'items': items[start_idx:end_idx],
                'total_pages': total_pages,
                'current_page': page,
                'has_prev': page > 0,
                'has_next': page < total_pages - 1
            }
            log_to_console(f"Directory content read successfully. Total items: {len(items)}, Pages: {total_pages}")
            return result
        except Exception as e:
            log_error(f"Error reading directory: {path}", e)
            return None

    @staticmethod
    def create_drives_keyboard():
        """Створити клавіатуру з дисками"""
        try:
            log_to_console("Creating drives keyboard")
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
            log_to_console("Drives keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error("Error creating drives keyboard", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_folder_keyboard(path, page=0):
        """Створити клавіатуру для папки"""
        try:
            log_to_console(f"Creating folder keyboard for: {path} (page {page})")
            keyboard = InlineKeyboardMarkup()
            content = FileExplorer.get_directory_content(path, page)
            
            if content is None:
                log_to_console(f"Access error for path: {path}", "WARNING")
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
            
            log_to_console(f"Folder keyboard created successfully for: {path}")
            return keyboard
        except Exception as e:
            log_error(f"Error creating folder keyboard for: {path}", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_file_keyboard(file_path):
        """Створити клавіатуру для файлу"""
        try:
            log_to_console(f"Creating file keyboard for: {file_path}")
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
            
            log_to_console(f"File keyboard created successfully for: {file_path}")
            return keyboard
        except Exception as e:
            log_error(f"Error creating file keyboard for: {file_path}", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def create_delete_confirmation_keyboard(file_path):
        """Створити клавіатуру підтвердження видалення"""
        try:
            log_to_console(f"Creating delete confirmation keyboard for: {file_path}")
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
            log_to_console("Delete confirmation keyboard created successfully")
            return keyboard
        except Exception as e:
            log_error(f"Error creating delete confirmation keyboard for: {file_path}", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def run_file(file_path):
        """Запустити файл"""
        try:
            log_to_console(f"Attempting to run file: {file_path}")
            os.startfile(file_path)
            log_to_console(f"File executed successfully: {file_path}")
            return True
        except Exception as e:
            log_error(f"Error running file: {file_path}", e)
            return False

    @staticmethod
    def delete_file(file_path):
        """Видалити файл"""
        try:
            log_to_console(f"Attempting to delete file: {file_path}")
            os.remove(file_path)
            log_to_console(f"File deleted successfully: {file_path}")
            return True
        except Exception as e:
            log_error(f"Error deleting file: {file_path}", e)
            return False 