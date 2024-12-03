import PyInstaller.__main__
import os

# Створюємо список файлів та папок для включення
additional_files = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('config.json', '.'),
]

# Формуємо команду для PyInstaller
command = [
    'main.py',  # Головний файл
    '--name=TamamoHub-Commander',  # Назва exe файлу
    '--onefile',  # Створити один exe файл
    '--windowed',  # Приховати консоль
    '--icon=icon.ico',  # Іконка (створіть або видаліть цей параметр)
    '--add-data=templates;templates',  # Додаємо папку templates
    '--add-data=static;static',  # Додаємо папку static
    '--add-data=config.json;.',  # Додаємо конфіг
    '--hidden-import=PyQt6.QtWebEngineCore',
    '--hidden-import=engineio.async_drivers.threading',
    '--hidden-import=PyQt6.QtGui',
    '--hidden-import=PyQt6.QtCore',
    '--hidden-import=PyQt6.QtWidgets',
    '--hidden-import=PyQt6.QtWebEngineWidgets',
    '--collect-all=telebot',
    '--collect-all=flask',
    '--collect-all=pyautogui',
    '--collect-all=psutil',
    '--collect-all=GPUtil',
    '--collect-all=pyttsx3',
    '--collect-all=googletrans',
    '--collect-all=gtts',
    '--collect-all=sympy',
]

# Запускаємо PyInstaller
PyInstaller.__main__.run(command) 