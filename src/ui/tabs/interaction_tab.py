from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from ai.gemini_client import GeminiClient
from ..widgets.loading_indicator import LoadingIndicator
from utils.ai_worker import AIWorker

class InteractionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Önce UI'ı kur
        try:
            self.ai_client = GeminiClient()
        except ValueError as e:
            self.show_error_message(str(e))
            self.compare_button.setEnabled(False)
        self.thread = None
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # İlaç giriş alanları
        drug1_layout = QHBoxLayout()
        self.drug1_input = QLineEdit()
        self.drug1_input.setPlaceholderText("1. İlaç adı...")
        drug1_layout.addWidget(QLabel("İlaç 1:"))
        drug1_layout.addWidget(self.drug1_input)
        
        drug2_layout = QHBoxLayout()
        self.drug2_input = QLineEdit()
        self.drug2_input.setPlaceholderText("2. İlaç adı...")
        drug2_layout.addWidget(QLabel("İlaç 2:"))
        drug2_layout.addWidget(self.drug2_input)
        
        # Karşılaştır butonu
        self.compare_button = QPushButton("Karşılaştır")
        self.compare_button.clicked.connect(self.check_interactions)
        
        # Sonuç alanı
        self.result_text = QTextEdit()
        self.result_text.setObjectName("responseArea")
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(400)
        
        # Yükleme göstergesi
        self.loading = LoadingIndicator(self)
        
        # Layout'a ekle
        layout.addLayout(drug1_layout)
        layout.addLayout(drug2_layout)
        layout.addWidget(self.compare_button)
        layout.addWidget(self.result_text)
        
    def format_response(self, response: str) -> str:
        formatted = "<div style='line-height: 1.6;'>"
        
        sections = response.split('\n\n')
        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                if not line.strip():
                    continue
                    
                if line[0].isdigit() and '.' in line:
                    # Ana başlıklar
                    title, content = line.split('.', 1)
                    formatted += f"<h3 style='color: #e74c3c; margin: 15px 0 10px 0;'>{title}.{content}</h3>"
                elif line.startswith('•') or line.startswith('-'):
                    # Alt maddeler
                    formatted += f"<p style='margin: 5px 0 5px 20px; color: #34495e;'>{line}</p>"
                else:
                    # Normal metin
                    formatted += f"<p style='margin: 5px 0; color: #34495e;'>{line}</p>"
        
        formatted += "</div>"
        return formatted
        
    def check_interactions(self):
        drug1 = self.drug1_input.text()
        drug2 = self.drug2_input.text()
        
        if drug1 and drug2 and not self.thread:
            try:
                if hasattr(self, 'main_window'):
                    self.main_window.show_waiting()
                
                prompt = f"""
                {drug1} ve {drug2} ilaçları arasındaki etkileşimi analiz et.
                
                Lütfen şu başlıklar altında detaylı bilgi ver:
                1. Etkileşim riski var mı?
                2. Varsa, ne tür etkileşimler olabilir?
                3. Hangi yan etkiler ortaya çıkabilir?
                4. Alınması gereken önlemler nelerdir?
                5. Her iki ilacın da kullanım amaçları nelerdir?
                6. Önemli uyarılar nelerdir?
                
                Bilgileri düzenli ve maddeler halinde ver.
                """
                
                # Worker ve thread oluştur
                self.thread = QThread()
                self.worker = AIWorker(self.ai_client, prompt, "interaction")
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
                self.compare_button.setEnabled(False)
                
            except Exception as e:
                self.handle_error(str(e))

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
        self.compare_button.setEnabled(True)

    def set_main_window(self, main_window):
        self.main_window = main_window 

    def show_error_message(self, message):
        QMessageBox.critical(
            self,
            "Hata",
            message + "\n\nLütfen Ayarlar sekmesinden API anahtarınızı girin."
        ) 