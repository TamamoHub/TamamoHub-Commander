import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox, QStyle, QMainWindow
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon, QDesktopServices, QAction
from ..utils.bot_control import shutdown_program

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.setup_ui()
        self.setup_tray()

    def setup_ui(self):
        self.setWindowTitle("TamamoHub Commander")
        self.setFixedSize(1100, 650)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        
        # Створюємо веб-вікно
        profile = QWebEngineProfile("my_profile")
        self.web_view = CustomWebView(profile)
        self.setCentralWidget(self.web_view)
        self.web_view.setUrl(QUrl("http://localhost:5000"))

    def setup_tray(self):
        # Створюємо системний трей
        self.tray_icon = QSystemTrayIcon(self)
        
        # Встановлюємо стандартну іконку
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        
        # Створюємо контекстне меню
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Показати")
        show_action.triggered.connect(self.show_window)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("Вийти")
        quit_action.triggered.connect(shutdown_program)
        
        # Встановлюємо меню
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def show_minimize_message(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("TamamoHub Commander")
        msg.setText("Програму згорнуто")
        msg.setInformativeText(
            "Програма продовжує працювати у фоні.\n"
            "Для відновлення використовуйте контекстне меню в треї (права кнопка миші).\n"
            "Для закриття використовуйте Диспетчер завдань Windows (Ctrl+Shift+Esc)."
        )
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1f2937;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4b5563;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6b7280;
            }
        """)
        
        msg.exec()

    def closeEvent(self, event):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("TamamoHub Commander")
        dialog.setText("Закриття програми")
        dialog.setInformativeText(
            "Виберіть дію:\n\n"
            "• Закрити - повністю завершити роботу\n"
            "• Згорнути - продовжити роботу у фоні\n"
            "• Скасувати - повернутися до програми\n\n"
            "⚠️ Увага: Якщо програму згорнуто у фоновий режим, "
            "закрити її можна буде лише через Диспетчер завдань Windows!"
        )
        
        close_button = dialog.addButton("Закрити", QMessageBox.ButtonRole.DestructiveRole)
        minimize_button = dialog.addButton("Згорнути", QMessageBox.ButtonRole.ActionRole)
        cancel_button = dialog.addButton("Скасувати", QMessageBox.ButtonRole.RejectRole)
        
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #1f2937;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                min-width: 100px;
                padding: 8px 16px;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                border: none;
                margin: 0 5px;
            }
            QPushButton[text="Закрити"] {
                background-color: #dc2626;
            }
            QPushButton[text="Закрити"]:hover {
                background-color: #ef4444;
            }
            QPushButton[text="Згорнути"] {
                background-color: #d97706;
            }
            QPushButton[text="Згорнути"]:hover {
                background-color: #f59e0b;
            }
            QPushButton[text="Скасувати"] {
                background-color: #4b5563;
            }
            QPushButton[text="Скасувати"]:hover {
                background-color: #6b7280;
            }
        """)
        
        dialog.exec()
        clicked_button = dialog.clickedButton()
        
        if clicked_button == close_button:
            event.accept()
            shutdown_program()
        elif clicked_button == minimize_button:
            event.ignore()
            self.hide()
            self.show_minimize_message()
        else:  # clicked_button == cancel_button
            event.ignore()

class CustomWebView(QWebEngineView):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self.page = CustomWebPage(self.profile)
        self.setPage(self.page)

class CustomWebPage(QWebEnginePage):
    def __init__(self, profile):
        super().__init__(profile)
        self.newWindowRequested.connect(self.handle_new_window)
        
    def handle_new_window(self, request):
        url = request.requestedUrl()
        QDesktopServices.openUrl(url)
        
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if url.host() != "127.0.0.1" and url.host() != "localhost":
            QDesktopServices.openUrl(url)
            return False
        return True

def create_window():
    window = MainWindow()
    window.show()
    return window