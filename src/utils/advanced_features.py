import os
import pyttsx3
import webbrowser
import sympy
from googletrans import Translator
from gtts import gTTS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Розширений словник заміни для покращення вимови
UKRAINIAN_REPLACEMENTS = {
    'привіт': 'прив+іт',
    'добрий': 'д+обрий',
    'день': 'д+ень',
    'дякую': 'дяк+ую',
    # Додайте інші слова за потреби
}

def improve_pronunciation(text):
    """
    Покращує вимову українських слів шляхом додавання наголосів
    та спеціальних символів для кращого розпізнавання
    """
    for word, replacement in UKRAINIAN_REPLACEMENTS.items():
        text = text.replace(word, replacement)
    return text

def get_best_ukrainian_voice(engine):
    """
    Знаходить найкращий доступний український голос
    """
    voices = engine.getProperty('voices')
    
    # Пріоритетний список мов
    priorities = ['ukrainian', 'ukr', 'rus', 'russian']
    
    for priority in priorities:
        for voice in voices:
            if priority in voice.name.lower():
                return voice
    
    # Якщо український голос не знайдено, повертаємо перший доступний
    return voices[0] if voices else None

class AdvancedFeatures:
    @staticmethod
    def create_menu_keyboard():
        """Створити головне меню розширених функцій"""
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("📝 Відправити текст", callback_data="advanced:text"),
            InlineKeyboardButton("🗣️ Озвучити текст", callback_data="advanced:tts")
        )
        keyboard.row(
            InlineKeyboardButton("🎤 Калькулятор", callback_data="advanced:calc"),
            InlineKeyboardButton("🌐 Відкрити посилання", callback_data="advanced:url")
        )
        keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_pc"))
        return keyboard

    @staticmethod
    def send_text_to_pc(text):
        """Відправити текст на ПК через буфер обміну"""
        try:
            import pyperclip
            pyperclip.copy(text)
            return "Текст скопійовано в буфер обміну"
        except Exception as e:
            return f"Помилка копіювання тексту: {str(e)}"

    @staticmethod
    def text_to_speech(text, lang='uk'):
        """Озвучити текст"""
        try:
            # Озвучування на ПК
            engine = pyttsx3.init()
            
            # Налаштування голосового движка
            engine.setProperty('volume', 1.0)  # Максимальна гучність
            engine.setProperty('rate', 150)    # Оптимальна швидкість
            
            # Шукаємо український голос
            voices = engine.getProperty('voices')
            ukrainian_voice = None
            for voice in voices:
                if 'ukrainian' in voice.name.lower() or 'ukr' in voice.name.lower():
                    ukrainian_voice = voice
                    break
            
            if ukrainian_voice:
                engine.setProperty('voice', ukrainian_voice.id)
            
            # Попередня обробка тексту для кращої вимови
            processed_text = text
            replacements = {
                'і': 'и',  # Заміна для кращої вимови
                'ї': 'йі',
                'є': 'йе',
                'щ': 'шч',
                'я': 'йа',
                'ю': 'йу',
                'ґ': 'г',
            }
            
            for old, new in replacements.items():
                processed_text = processed_text.replace(old, new)
            
            # Озвучуємо текст
            engine.say(processed_text)
            engine.runAndWait()
            
            # Створення аудіофайлу для Telegram
            tts = gTTS(text=text, lang=lang)
            filename = "speech.mp3"
            tts.save(filename)
            return filename
        except Exception as e:
            return f"Помилка озвучування: {str(e)}"

    @staticmethod
    def solve_math(expression):
        """Розв'язати математичний вираз"""
        try:
            # Використовуємо sympy для обчислень
            result = sympy.sympify(expression)
            return f"Результат: {result}"
        except Exception as e:
            return f"Помилка обчислення: {str(e)}"

    @staticmethod
    def open_url(url):
        """Відкрити URL в браузері за замовчуванням"""
        try:
            # Перевіряємо та форматуємо URL
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            webbrowser.open(url)
            return f"URL відкрито: {url}"
        except Exception as e:
            return f"Помилка відкриття URL: {str(e)}" 