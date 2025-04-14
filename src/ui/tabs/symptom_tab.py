from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                           QPushButton, QLabel, QMessageBox)
from ai.gemini_client import GeminiClient
from ..widgets.loading_indicator import LoadingIndicator
from PyQt6.QtCore import QThread
from utils.ai_worker import AIWorker

class SymptomTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Önce UI'ı kur
        try:
            self.ai_client = GeminiClient()
        except ValueError as e:
            self.show_error_message(str(e))
            self.analyze_button.setEnabled(False)
        self.thread = None
        
    def set_main_window(self, main_window):
        self.main_window = main_window
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Belirti giriş alanı
        self.symptom_label = QLabel("Belirtilerinizi yazın:")
        self.symptom_input = QTextEdit()
        self.symptom_input.setMaximumHeight(100)
        self.symptom_input.setPlaceholderText("Örnek: baş ağrısı, ateş, öksürük...")
        
        # Analiz butonu
        self.analyze_button = QPushButton("Belirtileri Analiz Et")
        self.analyze_button.clicked.connect(self.analyze_symptoms)
        
        # Detaylı bilgi alanı
        self.details_label = QLabel("Öneriler:")
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        
        # Yükleme göstergesi
        self.loading = LoadingIndicator(self)
        
        # Widget'ları layout'a ekleme
        layout.addWidget(self.symptom_label)
        layout.addWidget(self.symptom_input)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.details_label)
        layout.addWidget(self.details_text)
        
    def format_response(self, response: str) -> str:
        formatted = "<div style='line-height: 1.6;'>"
        
        sections = response.split('\n\n')
        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                if not line.strip():
                    continue
                    
                if "ÖNEMLİ" in line.upper() or "UYARI" in line.upper():
                    # Uyarılar
                    formatted += f"<p style='margin: 10px 0; padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 4px;'>{line}</p>"
                elif line[0].isdigit() and '.' in line:
                    # Ana başlıklar
                    title, content = line.split('.', 1)
                    formatted += f"<h3 style='color: #2980b9; margin: 15px 0 10px 0;'>{title}.{content}</h3>"
                elif line.startswith('•') or line.startswith('-'):
                    # Alt maddeler
                    formatted += f"<p style='margin: 5px 0 5px 20px; color: #34495e;'>{line}</p>"
                else:
                    # Normal metin
                    formatted += f"<p style='margin: 5px 0; color: #34495e;'>{line}</p>"
        
        formatted += "</div>"
        return formatted
        
    def analyze_symptoms(self):
        symptoms = self.symptom_input.toPlainText()
        if symptoms and not self.thread:
            try:
                if hasattr(self, 'main_window'):
                    self.main_window.show_waiting()
                
                # Worker ve thread oluştur
                self.thread = QThread()
                self.worker = AIWorker(self.ai_client, symptoms, "symptom")
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
                self.analyze_button.setEnabled(False)
                
            except Exception as e:
                self.handle_error(str(e))
    
    def handle_response(self, response):
        formatted_response = self.format_response(response)
        self.details_text.setHtml(formatted_response)
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
    
    def handle_error(self, error_message):
        self.details_text.setText(f"Hata oluştu: {error_message}")
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
        self.analyze_button.setEnabled(True)
    
    def cleanup(self):
        self.thread = None
        self.analyze_button.setEnabled(True)

    def show_error_message(self, message):
        QMessageBox.critical(
            self,
            "Hata",
            message + "\n\nLütfen Ayarlar sekmesinden API anahtarınızı girin."
        ) 