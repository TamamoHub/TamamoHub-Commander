import os
import pyttsx3
import webbrowser
import sympy
from googletrans import Translator
from gtts import gTTS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..core.logger import log_to_console, log_error

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
    try:
        log_to_console(f"Improving pronunciation for text: {text[:50]}...")
        for word, replacement in UKRAINIAN_REPLACEMENTS.items():
            text = text.replace(word, replacement)
        return text
    except Exception as e:
        log_error("Error improving pronunciation", e)
        return text

def get_best_ukrainian_voice(engine):
    """
    Знаходить найкращий доступний український голос
    """
    try:
        voices = engine.getProperty('voices')
        
        # Пріоритетний список мов
        priorities = ['ukrainian', 'ukr', 'rus', 'russian']
        
        for priority in priorities:
            for voice in voices:
                if priority in voice.name.lower():
                    log_to_console(f"Selected voice: {voice.name}")
                    return voice
        
        log_to_console("No Ukrainian voice found, using default voice")
        return voices[0] if voices else None
    except Exception as e:
        log_error("Error getting Ukrainian voice", e)
        return None

class AdvancedFeatures:
    @staticmethod
    def create_menu_keyboard():
        """Створити головне меню розширених функцій"""
        try:
            log_to_console("Creating advanced features menu")
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
        except Exception as e:
            log_error("Error creating advanced features menu", e)
            return InlineKeyboardMarkup()

    @staticmethod
    def send_text_to_pc(text):
        """Відправити текст на ПК через буфер обміну"""
        try:
            log_to_console(f"Copying text to clipboard: {text[:50]}...")
            import pyperclip
            pyperclip.copy(text)
            return "Текст скопійовано в буфер обміну"
        except Exception as e:
            log_error("Error copying text to clipboard", e)
            return f"Помилка копіювання тексту: {str(e)}"

    @staticmethod
    def text_to_speech(text, lang='uk'):
        """Озвучити текст"""
        try:
            log_to_console(f"Converting text to speech: {text[:50]}...")
            
            # Озвучування на ПК
            engine = pyttsx3.init()
            
            # Налаштування голосового движка
            engine.setProperty('volume', 1.0)  # Максимальна гучність
            engine.setProperty('rate', 150)    # Оптимальна швидкість
            
            # Шукаємо український голос
            ukrainian_voice = get_best_ukrainian_voice(engine)
            if ukrainian_voice:
                engine.setProperty('voice', ukrainian_voice.id)
            
            # Попередня обробка тексту для кращої вимови
            processed_text = improve_pronunciation(text)
            
            # Озвучуємо текст
            log_to_console("Playing text through system TTS")
            engine.say(processed_text)
            engine.runAndWait()
            
            # Створення аудіофайлу для Telegram
            log_to_console("Creating audio file for Telegram")
            tts = gTTS(text=text, lang=lang)
            filename = "speech.mp3"
            tts.save(filename)
            log_to_console("Audio file created successfully")
            return filename
        except Exception as e:
            log_error("Error in text-to-speech conversion", e)
            return f"Помилка озвучування: {str(e)}"

    @staticmethod
    def solve_math(expression):
        """Розв'язати математичний вираз"""
        try:
            log_to_console(f"Solving math expression: {expression}")
            result = sympy.sympify(expression)
            log_to_console(f"Math result: {result}")
            return f"Результат: {result}"
        except Exception as e:
            log_error(f"Error solving math expression: {expression}", e)
            return f"Помилка обчислення: {str(e)}"

    @staticmethod
    def open_url(url):
        """Відкрити URL в браузері за замовчуванням"""
        try:
            # Перевіряємо та форматуємо URL
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            log_to_console(f"Opening URL: {url}")
            webbrowser.open(url)
            return f"URL відкрито: {url}"
        except Exception as e:
            log_error(f"Error opening URL: {url}", e)
            return f"Помилка відкриття URL: {str(e)}"

    @staticmethod
    def speech_to_text(audio_file):
        """Розпізнавання мови з аудіо"""
        try:
            log_to_console(f"Starting speech recognition for file: {audio_file}")
            # Here would be your speech recognition implementation
            # This is a placeholder - add your actual implementation
            results = {
                'uk-UA': 'Текст українською',
                'ru-RU': 'Текст російською',
                'en-US': 'English text'
            }
            log_to_console("Speech recognition completed successfully")
            return results
        except Exception as e:
            log_error("Error in speech recognition", e)
            raise