from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QTextEdit, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from ai.gemini_client import GeminiClient
from utils.ai_worker import AIWorker

class ChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Önce UI'ı kur
        try:
            self.ai_client = GeminiClient()
        except ValueError as e:
            self.show_error_message(str(e))
            self.send_button.setEnabled(False)
        self.thread = None
        
    def set_main_window(self, main_window):
        self.main_window = main_window
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Bilgi etiketi
        self.info_label = QLabel(
            "Lütfen şikayetlerinizi detaylı bir şekilde anlatın. "
            "Acil durumlar için lütfen 112'yi arayın."
        )
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("""
            color: #e74c3c;
            padding: 10px;
            background-color: #fadbd8;
            border-radius: 4px;
            margin-bottom: 10px;
        """)
        
        # Sohbet geçmişi
        self.chat_history = QTextEdit()
        self.chat_history.setObjectName("chatHistory")
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumHeight(400)
        
        # Mesaj gönderme bölümü
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(80)
        self.message_input.setPlaceholderText("Mesajınızı yazın...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        
        self.send_button = QPushButton("Gönder")
        self.send_button.setMinimumWidth(100)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input, stretch=4)
        input_layout.addWidget(self.send_button, stretch=1)
        
        # Widget'ları layout'a ekleme
        layout.addWidget(self.info_label)
        layout.addWidget(self.chat_history)
        layout.addLayout(input_layout)
        
        # Enter tuşu ile mesaj gönderme
        self.message_input.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers():
                self.send_message()
                return True
        return super().eventFilter(obj, event)
        
    def send_message(self):
        message = self.message_input.toPlainText().strip()
        if message and not self.thread:
            try:
                if hasattr(self, 'main_window'):
                    self.main_window.show_waiting()
                
                # Kullanıcı mesajını göster
                self.chat_history.append(
                    f'<div style="margin-bottom: 10px;">'
                    f'<div style="color: #2c3e50; font-weight: bold;">Siz:</div>'
                    f'<div style="background-color: #e8f5e9; padding: 10px; border-radius: 4px; margin-top: 5px;">'
                    f'{message}</div></div>'
                )
                
                # Worker ve thread oluştur
                self.thread = QThread()
                self.worker = AIWorker(self.ai_client, message, "chat")
                self.worker.moveToThread(self.thread)
                
                # Sinyalleri bağla
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.handle_response)
                self.worker.error.connect(self.handle_error)
                self.worker.finished.connect(self.thread.quit)
                self.worker.error.connect(self.thread.quit)
                self.thread.finished.connect(self.cleanup)
                
                # Thread'i başlat
                self.thread.start()
                
                # Butonu devre dışı bırak
                self.send_button.setEnabled(False)
                
            except Exception as e:
                self.handle_error(str(e))
        
    def handle_response(self, response):
        self.chat_history.append(
            f'<div style="margin-bottom: 10px;">'
            f'<div style="color: #2980b9; font-weight: bold;">E-Eczacı:</div>'
            f'<div style="background-color: #e3f2fd; padding: 10px; border-radius: 4px; margin-top: 5px;">'
            f'{response}</div></div>'
        )
        self.message_input.clear()
        self.send_button.setEnabled(True)
        # Bekletme yazısını gizle
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
        
    def handle_error(self, error):
        self.chat_history.append(f"Hata oluştu: {error}")
        self.message_input.clear()
        self.send_button.setEnabled(True)
        # Bekletme yazısını gizle
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
        
    def cleanup(self):
        self.thread = None
        self.send_button.setEnabled(True)

    def show_error_message(self, message):
        QMessageBox.critical(
            self,
            "Hata",
            message + "\n\nLütfen Ayarlar sekmesinden API anahtarınızı girin."
        ) 