from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLineEdit, QPushButton, QTextEdit, QLabel,
                           QMessageBox)
from PyQt6.QtCore import Qt, QThread
from ai.gemini_client import GeminiClient
from utils.ai_worker import AIWorker
from ui.widgets.loading_indicator import LoadingIndicator

class DrugInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Önce UI'ı kur
        try:
            self.ai_client = GeminiClient()
        except ValueError as e:
            self.show_error_message(str(e))
            self.search_button.setEnabled(False)  # Butonu devre dışı bırak
        self.thread = None
    
    def set_main_window(self, main_window):
        self.main_window = main_window
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Arama bölümü
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("İlaç adı giriniz...")
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.search_drug)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        # Sonuç bölümü
        self.result_text = QTextEdit()
        self.result_text.setObjectName("responseArea")
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(400)
        
        # Yükleme göstergesi
        self.loading = LoadingIndicator(self)
        
        # Layout'a ekle
        layout.addLayout(search_layout)
        layout.addWidget(self.result_text)
        
    def format_response(self, response: str) -> str:
        formatted = """
        <div style='
            line-height: 1.8;
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 15px;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        '>
        """
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line[0].isdigit() and '.' in line:
                # Ana başlıklar
                title, content = line.split('.', 1)
                formatted += f"""
                    <div style='
                        background-color: #f8f9fa;
                        padding: 12px 15px;
                        margin: 15px 0;
                        border-left: 4px solid #3498db;
                        border-radius: 4px;
                    '>
                        <h3 style='
                            color: #2c3e50;
                            font-size: 18px;
                            margin: 0;
                        '>{title}.{content}</h3>
                    </div>
                """
            elif line.startswith('•') or line.startswith('-'):
                # Alt maddeler
                formatted += f"""
                    <div style='
                        margin: 8px 0 8px 25px;
                        padding: 8px 15px;
                        background-color: #f8f9fa;
                        border-radius: 4px;
                    '>
                        <p style='
                            color: #34495e;
                            margin: 0;
                        '>{line}</p>
                    </div>
                """
            elif "ÖNEMLİ" in line.upper() or "UYARI" in line.upper() or "DİKKAT" in line.upper():
                # Uyarılar
                formatted += f"""
                    <div style='
                        background-color: #fff3cd;
                        color: #856404;
                        padding: 12px 15px;
                        margin: 15px 0;
                        border-radius: 4px;
                        border-left: 4px solid #ffc107;
                    '>
                        <p style='margin: 0;'><strong>⚠️ {line}</strong></p>
                    </div>
                """
            else:
                # Normal metin
                formatted += f"""
                    <p style='
                        color: #2c3e50;
                        margin: 10px 0;
                        padding: 0 10px;
                    '>{line}</p>
                """
        
        formatted += "</div>"
        return formatted
        
    def search_drug(self):
        drug_name = self.search_input.text()
        if drug_name and not self.thread:  # Thread çalışmıyorsa
            try:
                if hasattr(self, 'main_window'):
                    self.main_window.show_waiting()
                
                prompt = f"""
                {drug_name} ilacı hakkında detaylı bilgi ver.
                Lütfen şu bilgileri içer:
                1. İlacın etken maddesi
                2. Kullanım amacı ve endikasyonları
                3. Kullanım talimatları
                4. Yan etkileri
                5. Dozaj bilgisi
                6. Önemli uyarılar
                7. Etkileşime girdiği ilaçlar
                
                Bilgileri düzenli ve maddeler halinde ver.
                """
                
                # Worker ve thread oluştur
                self.thread = QThread()
                self.worker = AIWorker(self.ai_client, prompt, "drug_info")
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
                
                # Arama butonunu devre dışı bırak
                self.search_button.setEnabled(False)
                
            except Exception as e:
                self.handle_error(str(e))
                if hasattr(self, 'main_window'):
                    self.main_window.hide_waiting()
    
    def handle_response(self, response):
        formatted_response = self.format_response(response)
        self.result_text.setHtml(formatted_response)
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
    
    def handle_error(self, error_message):
        self.result_text.setText(f"Hata oluştu: {error_message}")
        if hasattr(self, 'main_window'):
            self.main_window.hide_waiting()
    
    def cleanup(self):
        self.thread = None
        self.search_button.setEnabled(True)

    def show_error_message(self, message):
        QMessageBox.critical(
            self,
            "Hata",
            message + "\n\nLütfen Ayarlar sekmesinden API anahtarınızı girin."
        ) 