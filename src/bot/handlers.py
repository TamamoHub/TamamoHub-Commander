import os
import shutil
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from ..core.logger import log_to_console
from ..core.config import get_admin_id, set_admin_id
from ..utils.bot_control import shutdown_program, get_log_file
from ..utils.system_info import get_system_info
from ..utils.file_explorer import FileExplorer
from ..utils.task_manager import TaskManager
from ..utils.windows_commands import WindowsCommands
from ..utils.mouse_control import MouseControl
from ..utils.keyboard_control import KeyboardControl
from ..utils.advanced_features import AdvancedFeatures

def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("💻 Комп'ютер"),
        KeyboardButton("⚙️ Керування ботом")
    )
    return keyboard

def create_pc_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("🔒 Заблокувати"),
        KeyboardButton("🔌 Вимкнути")
    )
    keyboard.add(
        KeyboardButton("🔊 Гучність +"),
        KeyboardButton("🔈 Гучність -")
    )
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard

def create_bot_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("⭕ Завершити програму", callback_data="shutdown_program"),
        InlineKeyboardButton("📥 Завантажити лог", callback_data="download_log")
    )
    return keyboard

def create_pc_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📊 Показники ПК", callback_data="system_info"),
        InlineKeyboardButton("📂 Провідник", callback_data="file_explorer:drives")
    )
    keyboard.row(
        InlineKeyboardButton("⚙️ Диспетчер завдань", callback_data="taskman:main"),
        InlineKeyboardButton("🪟 Команди Windows", callback_data="wincmd:menu")
    )
    keyboard.row(
        InlineKeyboardButton("🖱️ Керування мишею", callback_data="mouse:control"),
        InlineKeyboardButton("⌨️ Клавіатура", callback_data="keyboard:menu")
    )
    keyboard.row(
        InlineKeyboardButton("🔧 Розширені функції", callback_data="advanced:menu")
    )
    return keyboard

def create_drives_keyboard():
    keyboard = InlineKeyboardMarkup()
    # Отримуємо список доступних дисків
    drives = [d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
             if os.path.exists(f"{d}:")]
    
    # Додаємо кнопки для кожного диску по 2 в ряд
    for i in range(0, len(drives), 2):
        row = []
        for drive in drives[i:i+2]:
            row.append(InlineKeyboardButton(
                f"{drive}:\\", 
                callback_data=f"explorer:drive:{drive}:"
            ))
        keyboard.row(*row)
    
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
    return keyboard

def create_folder_keyboard(path, page=0):
    keyboard = InlineKeyboardMarkup()
    items_per_page = 8
    
    try:
        # Отримуємо список файлів і папок
        items = os.listdir(path)
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        
        # Розбиваємо на сторінки
        total_pages = (len(items) - 1) // items_per_page + 1
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        current_items = items[start_idx:end_idx]
        
        # Додаємо кнопки для файлів і папок
        for item in current_items:
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
        
        # Додаємо навігаційні кнопки
        nav_buttons = []
        
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(
                "⬅️", callback_data=f"explorer:page:{path}:{page-1}"
            ))
            
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton(
                "➡️", callback_data=f"explorer:page:{path}:{page+1}"
            ))
            
        if nav_buttons:
            keyboard.row(*nav_buttons)
        
        # Додаємо кнопки навігації
        bottom_buttons = []
        if os.path.dirname(path) != path:  # Якщо не корінь диску
            bottom_buttons.append(InlineKeyboardButton(
                "⬅️ Назад", 
                callback_data=f"explorer:folder:{os.path.dirname(path)}"
            ))
        
        bottom_buttons.append(InlineKeyboardButton(
            "💿 До дисків", 
            callback_data="explorer:drives"
        ))
        
        keyboard.row(*bottom_buttons)
        
    except Exception as e:
        keyboard.row(InlineKeyboardButton(
            "⚠️ Помилка доступу", 
            callback_data="explorer:drives"
        ))
    
    return keyboard

def create_file_keyboard(file_path):
    keyboard = InlineKeyboardMarkup()
    
    # Кнопки дій з файлом
    keyboard.row(
        InlineKeyboardButton("▶️ Запустити", callback_data=f"file:run:{file_path}"),
        InlineKeyboardButton("⬇️ Завантажити", callback_data=f"file:download:{file_path}")
    )
    keyboard.row(InlineKeyboardButton(
        "🗑️ Видалити", callback_data=f"file:delete:{file_path}"
    ))
    
    # Кнопки навігації
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

def create_system_info_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🔄 Оновити", callback_data="update_system_info"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc")
    )
    return keyboard

def is_admin(message):
    admin_id = get_admin_id()
    return admin_id and message.from_user.id == admin_id

def setup_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        admin_id = get_admin_id()
        if not admin_id:
            set_admin_id(message.from_user.id)
            log_to_console(f"Встановлено нового адміністратоа: {message.from_user.username} (ID: {message.from_user.id})")
            bot.reply_to(
                message,
                "Вітаю! Ви встановлені як адміністратор бота. Виберіть опцію:",
                reply_markup=create_main_keyboard()
            )
        elif message.from_user.id == admin_id:
            bot.reply_to(
                message,
                "Вітаю! Виберіть опцію:",
                reply_markup=create_main_keyboard()
            )
        else:
            bot.reply_to(
                message,
                f"Вибачте, але цей бот налаштований для використання тільки одним користувачем (ID: {admin_id})."
            )

    @bot.message_handler(func=lambda message: not is_admin(message))
    def unauthorized(message):
        admin_id = get_admin_id()
        if admin_id:
            bot.reply_to(
                message,
                f"Вибачте, але цей бот налаштований для використання тільки одним користувачем (ID: {admin_id})."
            )
        else:
            set_admin_id(message.from_user.id)
            log_to_console(f"Встановлено новоо адміністратора: {message.from_user.username} (ID: {message.from_user.id})")
            bot.reply_to(
                message,
                "Вітаю! Ви встановлені як адміністратор бота. Виберіть опцію:",
                reply_markup=create_main_keyboard()
            )

    @bot.message_handler(func=lambda message: message.text == "⚙️ Керування ботом")
    def bot_control(message):
        if not is_admin(message):
            return
        try:
            log_to_console(f"Користувач {message.from_user.username} відкрив меню керування ботом")
            keyboard = create_bot_inline_keyboard()
            bot.send_message(
                message.chat.id,
                "Функції керування ботом:",
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        except Exception as e:
            log_to_console(f"Помилка створення меню керування: {str(e)}")
            bot.reply_to(message, "Сталася помилка при створенні меню")

    @bot.message_handler(func=lambda message: message.text == "💻 Комп'ютер")
    def pc_control(message):
        if not is_admin(message):
            return
        log_to_console(f"Користувач {message.from_user.username} відкрив меню керування ПК")
        bot.send_message(
            message.chat.id,
            "Оберіть дію для керування комп'ютером:",
            reply_markup=create_pc_inline_keyboard()
        )

    # Переміщуємо функцію всередину setup_handlers
    def start_new_process(message):
        if not is_admin(message):
            return
            
        process_name = message.text.strip()
        if TaskManager.start_process(process_name):
            bot.reply_to(message, f"Процес {process_name} запущено")
        else:
            bot.reply_to(message, f"Помилка запуску процесу {process_name}")
        
        # Повертаємось до меню диспетчера завдань
        bot.send_message(
            message.chat.id,
            "Диспетчер завдань:",
            reply_markup=TaskManager.create_task_manager_keyboard()
        )

    # Оновлений обробник inline кнопок
    @bot.callback_query_handler(func=lambda call: True)
    def handle_inline_buttons(call):
        try:
            admin_id = get_admin_id()
            if not admin_id or call.from_user.id != admin_id:
                bot.answer_callback_query(call.id, "Доступ заборонено")
                return

            # Додаємо обробку кнопок керування ботом
            if call.data == "shutdown_program":
                bot.answer_callback_query(call.id, "Завершення роботи програми...")
                bot.edit_message_text(
                    "⚠️ Програму завершено",
                    call.message.chat.id,
                    call.message.message_id
                )
                shutdown_program()

            elif call.data == "download_log":
                log_file = get_log_file()
                if log_file and os.path.exists(log_file):
                    with open(log_file, 'rb') as f:
                        bot.send_document(
                            call.message.chat.id,
                            f,
                            caption="📄 Лог файл"
                        )
                    os.remove(log_file)  # Видаляємо тимчасовий файл
                    bot.answer_callback_query(call.id, "Лог файл відправлено")
                else:
                    bot.answer_callback_query(call.id, "Помилка отримання лог файлу")

            elif call.data == "back_to_pc":
                # Повернення до головного меню ПК
                bot.edit_message_text(
                    "Оберіть дію для керування комп'ютером:",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=create_pc_inline_keyboard()
                )

            elif call.data == "file_explorer:drives" or call.data == "explorer:drives":
                bot.edit_message_text(
                    "Виберіть диск:",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=FileExplorer.create_drives_keyboard()
                )
                
            elif call.data.startswith("explorer:"):
                _, action, *params = call.data.split(":")
                
                if action == "drive":
                    drive = params[0]
                    path = f"{drive}:\\"
                    bot.edit_message_text(
                        f"📂 {path}",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=FileExplorer.create_folder_keyboard(path)
                    )
                    
                elif action == "folder":
                    path = ":".join(params)
                    bot.edit_message_text(
                        f"📂 {path}",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=FileExplorer.create_folder_keyboard(path)
                    )
                    
                elif action == "file":
                    file_path = ":".join(params)
                    bot.edit_message_text(
                        f"📄 {os.path.basename(file_path)}",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=FileExplorer.create_file_keyboard(file_path)
                    )
                    
                elif action == "page":
                    path = ":".join(params[:-1])
                    page = int(params[-1])
                    bot.edit_message_text(
                        f"📂 {path}",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=FileExplorer.create_folder_keyboard(path, page)
                    )
                    
            elif call.data.startswith("taskman:"):
                _, action, *params = call.data.split(":")
                
                if action == "main":
                    bot.edit_message_text(
                        "Диспетчер завдань:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=TaskManager.create_task_manager_keyboard()
                    )
                    
                elif action == "new":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть назву процесу для запуску (наприклад, notepad.exe):"
                    )
                    bot.register_next_step_handler(call.message, start_new_process)
                    
                elif action == "list":
                    page = int(params[0]) if params else 0
                    bot.edit_message_text(
                        "Запущені процеси:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=TaskManager.create_process_list_keyboard(page)
                    )
                    
                elif action == "process":
                    pid = int(params[0])
                    bot.send_message(
                        call.message.chat.id,
                        f"Керування процесом (PID: {pid}):",
                        reply_markup=TaskManager.create_process_control_keyboard(pid)
                    )
                    
                elif action == "kill":
                    pid = int(params[0])
                    if TaskManager.kill_process(pid):
                        bot.answer_callback_query(call.id, "Процес завершено")
                        bot.send_message(
                            call.message.chat.id,
                            "Запущені процеси:",
                            reply_markup=TaskManager.create_process_list_keyboard(0)
                        )
                    else:
                        bot.answer_callback_query(call.id, "Помилка завершення процесу")
                        
                elif action == "restart":
                    pid = int(params[0])
                    if TaskManager.restart_process(pid):
                        bot.answer_callback_query(call.id, "Процес перезапущено")
                        bot.send_message(
                            call.message.chat.id,
                            "Запущені процеси:",
                            reply_markup=TaskManager.create_process_list_keyboard(0)
                        )
                    else:
                        bot.answer_callback_query(call.id, "Помилка перезапуску процесу")

            elif call.data.startswith("wincmd:"):
                _, command = call.data.split(":")
                
                if command == "menu":
                    bot.edit_message_text(
                        "Оберіть команду Windows:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=WindowsCommands.create_commands_keyboard()
                    )
                else:
                    result = WindowsCommands.execute_command(command)
                    if command == "screenshot":
                        with open(result, 'rb') as photo:
                            bot.send_photo(
                                call.message.chat.id,
                                photo,
                                caption="Скріншот екрану"
                            )
                        os.remove(result)
                    bot.answer_callback_query(call.id, result)

            elif call.data == "system_info" or call.data == "update_system_info":
                bot.answer_callback_query(call.id)
                info = get_system_info()
                bot.edit_message_text(
                    info,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown',
                    reply_markup=create_system_info_keyboard()
                )

            elif call.data.startswith("mouse:"):
                _, command, *args = call.data.split(":")
                
                if command == "control":
                    bot.edit_message_text(
                        "Керування мишею:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=MouseControl.create_mouse_keyboard()
                    )
                elif command == "speed":
                    bot.edit_message_text(
                        "Виберіть швидкість миші:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=MouseControl.create_speed_keyboard()
                    )
                else:
                    result = MouseControl.execute_command(command, *args)
                    bot.answer_callback_query(call.id, result)

            elif call.data.startswith("keyboard:"):
                _, command, *args = call.data.split(":")
                
                if command == "menu":
                    bot.edit_message_text(
                        "Керування клавіатурою:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=KeyboardControl.create_keyboard_menu()
                    )
                elif command == "function_keys":
                    bot.edit_message_text(
                        "Функціональні клавіші:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=KeyboardControl.create_function_keys_keyboard()
                    )
                elif command == "hotkeys":
                    bot.edit_message_text(
                        "Гарячі клавіші:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=KeyboardControl.create_hotkeys_keyboard()
                    )
                elif command == "special":
                    bot.edit_message_text(
                        "Спеціальні клавіші:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=KeyboardControl.create_special_keyboard()
                    )
                elif command == "input_text":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть текст, який потрібно набрати на комп'ютері:"
                    )
                    bot.register_next_step_handler(call.message, handle_keyboard_input)
                else:
                    result = KeyboardControl.execute_command(command, *args)
                    bot.answer_callback_query(call.id, result)

            elif call.data.startswith("advanced:"):
                _, command = call.data.split(":")
                
                if command == "menu":
                    bot.edit_message_text(
                        "Розширені функції:",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=AdvancedFeatures.create_menu_keyboard()
                    )
                elif command == "text":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть текст для відправки на ПК:"
                    )
                    bot.register_next_step_handler(call.message, handle_pc_text)
                elif command == "tts":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть текст для озвучування:"
                    )
                    bot.register_next_step_handler(call.message, handle_tts)
                elif command == "calc":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть математичний вираз:"
                    )
                    bot.register_next_step_handler(call.message, handle_math)
                elif command == "url":
                    bot.send_message(
                        call.message.chat.id,
                        "Введіть URL для відкриття:"
                    )
                    bot.register_next_step_handler(call.message, handle_url)

        except Exception as e:
            log_to_console(f"Помилка обробки inline кнопки: {str(e)}")
            bot.answer_callback_query(call.id, "Сталася помилка при виконанні команди")

    # Додаємо функцію обробки введеного тексту
    def handle_keyboard_input(message):
        if not is_admin(message):
            return
        
        text = message.text.strip()
        if text:
            result = KeyboardControl.execute_command("type", text)
            bot.reply_to(message, result)
        
        # Повертаємось до меню клавіатури
        bot.send_message(
            message.chat.id,
            "Керування клавіатурою:",
            reply_markup=KeyboardControl.create_keyboard_menu()
        )

    # Додаємо обробники повідомлень
    def handle_pc_text(message):
        if not is_admin(message):
            return
        text = message.text.strip()
        if text:
            result = AdvancedFeatures.send_text_to_pc(text)
            bot.reply_to(message, result)

    def handle_tts(message):
        if not is_admin(message):
            return
        text = message.text.strip()
        if text:
            filename = AdvancedFeatures.text_to_speech(text)
            if filename.endswith('.mp3'):
                with open(filename, 'rb') as audio:
                    bot.send_voice(message.chat.id, audio)
                os.remove(filename)
            else:
                bot.reply_to(message, filename)  # Це повідомлення про помилку

    def handle_math(message):
        if not is_admin(message):
            return
        expression = message.text.strip()
        if expression:
            result = AdvancedFeatures.solve_math(expression)
            bot.reply_to(message, result)

    def handle_url(message):
        if not is_admin(message):
            return
        url = message.text.strip()
        if url:
            result = AdvancedFeatures.open_url(url)
            bot.reply_to(message, result)

    # Додаємо обробник голосових повідомлень
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        if not is_admin(message):
            return
        
        try:
            # Завантажуємо голосове повідомлення
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Зберігаємо його
            voice_file = "voice_message.ogg"
            with open(voice_file, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            # Розпізнаємо текст
            results = AdvancedFeatures.speech_to_text(voice_file)
            
            # Формуємо відповідь
            response = "Розпізнаний текст:\n\n"
            response += "🇺🇦 Українська: " + results.get('uk-UA', '---') + "\n"
            response += "🇷🇺 Російська: " + results.get('ru-RU', '---') + "\n"
            response += "🇺🇸 Англійська: " + results.get('en-US', '---')
            
            bot.reply_to(message, response)
            
            # Видаляємо тимчасовий файл
            os.remove(voice_file)
            
        except Exception as e:
            bot.reply_to(message, f"Помилка розпізнавання: {str(e)}")

    # ... (інші обробники для керування ПК залишаються без змін)